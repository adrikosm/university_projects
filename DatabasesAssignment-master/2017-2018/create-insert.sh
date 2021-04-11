#!/bin/bash
# shellcheck disable=SC2068,SC2207

METAR_URL='http://www.metar.org/upload/metar.php'
GOOGLE_API='https://maps.googleapis.com/maps/api/geocode/json'
GOOGLE_KEY='AIzaSyCfvPXOXa8X-g3msh9qj6HH0hv0awfTKUc'

# Check dependencies
check_deps() {
  _print_dep() {
    printf '%s %s %s\n' >&2 \
      'You need to install' "$1" \
      'before using this script.'
  }
  local miss=0
  if ! command -v hxnormalize >/dev/null; then
    _print_dep 'html-xml-utils'
    ((++miss))
  fi
  if ! command -v w3m >/dev/null; then
    _print_dep 'w3m'
    ((++miss))
  fi
  unset -f _print_dep
  # Exit if missing
  ((miss)) && exit 1
  return 0
}

# Get weather info from metar
get_weather() {
  curl -Ss "$METAR_URL" | \
    hxnormalize -x 2>/dev/null | \
    hxselect 'td' | \
    w3m -dump -cols 1000 -T 'text/html' | \
    sed -e '/\[.*\]/,+1d' -e 'N;N;s/\n/ /g'
}

# Get station location from Google's API
get_location() {
  local address
  address="$(tr ' ' '+' <<< "$1"),$2"
  sleep 0.4
  curl -Ss -X GET "${GOOGLE_API}?key=${GOOGLE_KEY}&address=${address}" | \
    awk 'BEGIN {IFS=":"} /"location"/ {for(i=1; i<=2; ++i) {getline; gsub(/,/, ""); printf "%s ", $3}}'
}

# Create inserts in insert.sql script
create_inserts() {
  # Generic insert
  _insert() {
    local insert="INSERT INTO $1 ($2) VALUES ($3,"
    # Don't do anything if line exists
    if ! grep -qsF "$insert" scripts/insert.sql; then
      printf '%s %s);\n' "$insert" "$4" >> scripts/insert.sql
    fi
  }
  # Special insert for station
  _station() {
    local insert locat lat lon
    insert="$(printf "%s (%s) VALUES('%s'," 'INSERT INTO WEATHER_STATION' \
      'City, Prefecture, StationOP, Altitude, Latitude, Longitude' "$1")"
    # Don't do anything if line exists
    if ! grep -qsF "$insert" scripts/insert.sql; then
      locat="$(get_location "$1" "$2")"
      lat="$(cut -d ' ' -f1 <<< "$locat" | grep -Eo '[0-9]{2}\.[0-9]{1,6}')"
      lon="$(cut -d ' ' -f2 <<< "$locat" | grep -Eo '[0-9]{2}\.[0-9]{1,6}')"
      printf "%s %s, %s, %s);\n" >> scripts/insert.sql \
        "$insert" "'$2'" "$3" "'${lat:-null}', '${lon:-null}'"
    fi
  }
  local weather=()
  local cities=()
  IFS=$'\n' weather=("$(get_weather)")
  # Parse station data
  for line in ${weather[@]}; do
    pref="${line%% *}"
    _tmp="${line##$pref  }"
    city="${_tmp%%[A-Z].*}"
    cities+=("$city")
    _tmp="${_tmp##$city}"
    oper="${_tmp%%[0-9]*}"
    _tmp="${_tmp##$oper}"
    alt="${_tmp%% *}"
    _station "$city" "$pref" "'$oper', '$alt'"
  done
  # Parse remaining data
  IFS=$'\n' \
    fields=($(awk -F'[ ]' '{print $(NF-9)" "$(NF-7)" "$(NF-6)" "$(NF-4)" "$(NF-3)" "$(NF-2)}' \
    <<< "${weather[@]}"))
  local count=0
  for field in ${fields[@]}; do
    city="${cities[count]}"
    date_time="TO_DATE('$(awk -F'[ ]' '{print $1" "$2}' <<< "$field")', 'DD/MM/YY HH24:MI')"
    temp="$(awk -F'[ ]' '{print $3}' <<< "$field")"
    hum="$(awk -F'[ ]' '{print $4}' <<< "$field")"
    press="$(awk -F'[ ]' '{print $5}' <<< "$field")"
    wind="$(awk -F'[ ]' '{print $6}' <<< "$field")"
    # Add sensors and measurements if they are non-null
    if [ -n "$temp" ]; then
      serial="$(tr -dc '0-9' < /dev/urandom | fold -w6 | grep -Ev '^0' -m1)"
      model="$(tr -dc 'A-Z-0-9' < /dev/urandom | fold -w100 | grep -Eo '[A-Z]{5}-[0-9]{3}$' -m1)"
      min_temp="-$(( RANDOM % (60 - 50 + 1) + 50 )).0"
      max_temp="$(( RANDOM % (80 - 60 + 1) + 60 )).9"
      _insert 'SENSOR' 'SerialNumber, CityPlaced, SensorModel, MinimValue, MaximValue, Unit, SensorType' \
        "$serial" "'$city', '$model', $min_temp, $max_temp, '°C', 'Temperature'"
      _insert 'MEASUREMENT' 'DateTime, SensorID, MeasValue' "$date_time, $serial" "$temp"
    fi
    if [ -n "$hum" ]; then
      serial="$(tr -dc '0-9' < /dev/urandom | fold -w6 | grep -Ev '^0' -m1)"
      model="$(tr -dc 'A-Z-0-9' < /dev/urandom | fold -w100 | grep -Eo '[A-Z]{5}-[0-9]{4}$' -m1)"
      _insert 'SENSOR' 'SerialNumber, CityPlaced, SensorModel, MinimValue, MaximValue, Unit, SensorType' \
        "$serial" "'$city', '$model', 0, 100, '%', 'Humidity'"
      _insert 'MEASUREMENT' 'DateTime, SensorID, MeasValue' "$date_time, $serial" "$hum"
    fi
    if [ -n "$press" ]; then
      serial="$(tr -dc '0-9' < /dev/urandom | fold -w5 | grep -Ev '^0' -m1)"
      model="$(tr -dc 'A-Z-0-9' < /dev/urandom | fold -w100 | grep -Eo '[A-Z]{4}-[0-9]{3}$' -m1)"
      min_press="$(( RANDOM % (750 - 700 + 1) + 700 )).0"
      max_press="$(( RANDOM % (1100 - 1050 + 1) + 1050 )).9"
      _insert 'SENSOR' 'SerialNumber, CityPlaced, SensorModel, MinimValue, MaximValue, Unit, SensorType' \
        "$serial" "'$city', '$model', $min_press, $max_press, 'hPa', 'Pressure'"
      _insert 'MEASUREMENT' 'DateTime, SensorID, MeasValue' "$date_time, $serial" "$press"
    fi
    if [ -n "$wind" ]; then
      serial="$(tr -dc '0-9' < /dev/urandom | fold -w5 | grep -Ev '^0' -m1)"
      model="$(tr -dc 'A-Z-0-9' < /dev/urandom | fold -w100 | grep -Eo '[A-Z]{4}-[0-9]{4}$' -m1)"
      max_wind="$(( RANDOM % (25 - 20 + 1) + 20 )).9"
      _insert 'SENSOR' 'SerialNumber, CityPlaced, SensorModel, MinimValue, MaximValue, Unit, SensorType' \
        "$serial" "'$city', '$model', 0.0, $max_wind, 'km/h', 'Wind'"
      _insert 'MEASUREMENT' 'DateTime, SensorID, MeasValue' "$date_time, $serial" "$wind"
    fi
    ((++count));
  done
  printf '\nCOMMIT;\n' >> scripts/insert.sql
}

# Create statistics for each day and month
create_stats() {
  local curdate
  curdate="$(date +%d/%m/%y)"
  # Insert or update statistics using merge
  _merge() {
    local stat_type
    [ "$1" = 'DAY' ] && stat_type='DAILY' || stat_type='MONTHLY'
    printf '\n%s\n%s %s\n%s\n%s\n%s\n%s\n%s %s %s %s\n%s %s;\n' >> scripts/insert.sql \
      "MERGE INTO ${stat_type}_STATISTICS" \
      'USING (SELECT S.CITYPLACED AS City, MIN(M.MEASVALUE) AS Minim, MAX(M.MEASVALUE) AS Maxim,' \
      "ROUND(AVG(M.MEASVALUE),1) AS Avrg, S.SENSORTYPE AS S_Type, TO_CHAR(M.DATETIME, '$3') AS CurDate" \
      'FROM MEASUREMENT M INNER JOIN SENSOR S ON M.SENSORID = S.SERIALNUMBER' \
      "WHERE TO_CHAR(M.DATETIME, '$3') = '$2'" \
      "GROUP BY S.CITYPLACED, S.SENSORTYPE, TO_CHAR(M.DATETIME, '$3')) TMP" \
      "ON (TMP.City = ${1:0:1}_STATCITY AND TMP.CurDate = TO_CHAR(${1}ID, '$3') AND TMP.S_Type = ${1:0:1}_STATTYPE)" \
      'WHEN NOT MATCHED THEN' \
      "INSERT (${1}ID, ${1:0:1}_STATCITY, ${1:0:1}_STATMIN," \
      "${1:0:1}_STATMAX, ${1:0:1}_STATAVG, ${1:0:1}_STATTYPE)" \
      "VALUES (TO_DATE(TMP.CurDate, '$3'), TMP.City, TMP.Minim, TMP.Maxim, TMP.Avrg, TMP.S_Type)" \
      'WHEN MATCHED THEN UPDATE' \
      "SET ${1:0:1}_STATMIN = TMP.Minim, ${1:0:1}_STATMAX = TMP.Maxim, ${1:0:1}_STATAVG = TMP.Avrg"
  }
  _merge 'MONTH' "${curdate:3}" 'MM/YY'
  _merge 'DAY' "$curdate" 'DD/MM/YY'
  printf '\nCOMMIT;\n\n' >> scripts/insert.sql
}

# Exit if not running in a terminal
if ! tty -s; then
  printf 'This script must be ran in a terminal!' >&2
  exit 1
fi

check_deps
mkdir -p scripts
# Get data every hour
while :; do
  printf 'Gathering data...\n'
  create_inserts
  create_stats
  printf 'Waiting for an hour...\n'
  sleep 3600
done

# Sources:
# https://joeferner.github.io/2015/07/15/linux-command-line-html-and-awk/
# https://stackoverflow.com/a/16906481
# https://askubuntu.com/questions/863572
# https://gist.github.com/earthgecko/3089509
# https://stackoverflow.com/questions/12903446

