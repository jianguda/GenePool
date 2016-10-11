# GenePool
Wash traditional tags and obtain plot tags and comment tags of various movies, also build a demo platform

__Notice: GenePool is not complete for related secrecy agreement. However, a demo platform is provided and it is easy to build to know the effect of GenePool.__

## Project
GenePool is only a portion of original project, it acted as a demo platform. PyCharm is recommended to deploy the server. MongoDB is needed as a database.

## Quick Understanding
This section is suitable for those who just want to know GenePool but is not ready to reuse it. Just read the only .pdf file.

## How to Build
Install MongoDB firstly, then create a db named 'display'. Use 'mongoimport' to import all __jsonArray__ files in /boot to the db. Action, names of collections should be set referring the mapping table below.

| names of jsonArray files | names of corresponding collections |
| ------------- | ------------- |
| boot_comment_a.txt | comment_a |
| boot_comment_b.txt | comment_b |
| boot_gather.txt | boot_gather |
| boot_media.txt | boot_media |
| boot_segment_a.txt | segment_a |
| boot_segment_b.txt | segment_b |
| boot_static_a.txt | static_a |
| boot_static_b.txt | static_b |
| boot_table_ns.txt | table_ns |
| boot_table_nt.txt | table_nt |
| boot_table_oa.txt | table_oa |
| boot_table_ot.txt | table_ot |
| boot_trans_a.txt | trans_a |
| boot_trans_b.txt | trans_b |

After doing that, make sure the mongodb service is running. Then run the /tmall/display.py to deploy the server. Access this demo platform by visiting the localhost:8000.
