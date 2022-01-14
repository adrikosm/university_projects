select *
from   table-with-xml-column t
,      xmltable
       ( 'all.xml'
         passing t.xml_column_name
         columns column1 number       path 'path1'
         columns column2 char(1 byte) path 'path2'
         columns column3 varchar2(30) path 'path3'
       ) t2

