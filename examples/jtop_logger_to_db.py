#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# This file is part of the jetson_stats package (https://github.com/rbonghi/jetson_stats or http://rnext.it).
# Copyright (c) 2019 Raffaello Bonghi.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from jtop import jtop, JtopException
import sqlite3
import argparse

data_types_dict = {'int':'INTEGER', 'float':'REAL','timedelta':'TEXT', 'str':'TEXT', 'datetime':'TEXT', 'bytes':'BLOB'}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simple jtop logger')
    # Standard file to store the logs
    parser.add_argument('--file', action="store", dest="file", default="log.db")
    args = parser.parse_args()

    print("Simple jtop logger")
    print("Saving log on {file}".format(file=args.file))

    try:
        with jtop() as jetson:
            # Make csv file and setup csv
            con = sqlite3.connect(args.file)
            stats = jetson.stats
            data_types = [type(x) for x in stats]
            key_list = stats.keys()
            #key_list = [k.replace(' ', '_') for k in stats.keys()]
            column_list =[]
            for k in key_list:
                column_list.append("%s %s"%(k.replace(' ','_'), data_types_dict[type(stats[k]).__name__]))
            #print(stats)
            table_create_query = '''CREATE TABLE jtop (%s)'''%','.join(column_list)
            print(table_create_query)
            cur = con.cursor()
            cur.execute(table_create_query)
            while jetson.ok():
                stats = jetson.stats
                keys = [k.replace(' ', '_') for k in key_list]
                values = [stats[k] for k in key_list]
                row_insert_query = '''INSERT INTO jtop (%s) VALUES (%s)'''%(','.join(keys), ','.join(str(values)) 
                cur.execute(row_insert_query)
            con.commit()
            con.close()
            '''

            with open(args.file, 'w') as csvfile:
                stats = jetson.stats
                # Initialize cws writer
                writer = csv.DictWriter(csvfile, fieldnames=stats.keys())
                # Write header
                writer.writeheader()
                # Write first row
                writer.writerow(stats)
                # Start loop
                while jetson.ok():
                    stats = jetson.stats
                    # Write row
                    writer.writerow(stats)
                    print("Log at {time}".format(time=stats['time']))
                    '''
    except JtopException as e:
        print(e)
    except KeyboardInterrupt:
        print("Closed with CTRL-C")
    except IOError:
        print("I/O error")
# EOF
