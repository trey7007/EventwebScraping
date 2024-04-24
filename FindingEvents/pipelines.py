# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
from datetime import datetime


class FindingConcertsPipeline:

    def process_item(self, item, spider):

        adapter = ItemAdapter(item)


        ##Convert all data to strings
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            if value and (isinstance(value,tuple) or isinstance(value,list)):
                adapter[field_name] = value[0]


        ## Split up the Date and Time
        datetimesplit = adapter.get("datetime")
        
        time = ""

        for i in range(len(datetimesplit)):
            if datetimesplit[i] == "-":
                time = datetimesplit[i+2:]
                break

        adapter["time"] = time
        

        ## Format Date to actual SQL date

        date = adapter.get("date")

        date_fomatted = datetime.strptime(date, '%b %d, %Y')

        adapter["date"] = date_fomatted
        
        return item


class SaveEventsToSQLPipeline:

    def __init__(self):

            ## Create/Connect to database
            self.con = sqlite3.connect('eventdata.db')

            ## Create cursor, used to execute commands
            self.cur = self.con.cursor()

            ## Create quotes table if none exists
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS events(
                    event TEXT,
                    city TEXT,
                    name TEXT,
                    location TEXT,
                    date DATE,
                    time TEXT,
                    genre TEXT,
                    PRIMARY KEY (name, date)            
                )
            """)

    def close_spider(self,spider):
        self.cur.close()
        self.con.close()

 
    def process_item(self, item, spider):

        self.cur.execute("""
            SELECT COUNT(*) FROM events WHERE name = ? AND time = ?
        """, (item['name'], item['time']))

        # Fetch the result
        result = self.cur.fetchone()

        # If no record exists with the same [name, time], insert the data into the table
        if result[0] == 0:
            self.cur.execute("""
                    INSERT INTO events (event, city, name, location, date, time , genre) VALUES (?, ?, ?, ?, ?, ?, ?)  
                """,
                (
                    item['event'],
                    item['city'],
                    item['name'],
                    item['location'],
                    item['date'],
                    item['time'],
                    item['genre']
                ))

            self.con.commit()
        return item
       