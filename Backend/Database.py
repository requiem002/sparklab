#! /usr/bin/python3

#create a database class to handle the database connection and queries
# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import Error
from pydantic import BaseModel, ValidationError
import os
import json

class Database:
    def __init__(self, db_file):
        """ create a database connection to a SQLite database """
        self.conn = None
        self.db_file = db_file
        self.create_connection()

    def create_connection(self):
        """ create a database connection to a SQLite database """
        try:
            self.conn = sqlite3.connect(self.db_file)
            print(f"Connected to {self.db_file} successfully.")
        except Error as e:
            print(e)
    def create_table(self):
        """ create a table from the create_table_sql statement """
        try:
            cursor = self.conn.cursor()
            cursor.execute( "CREATE TABLE IF NOT EXISTS components (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, serialID Text, category TEXT,sub_category TEXT,cabinet_ID TEXT,location TEXT,quantity INTEGER, value TEXT);")
            print("Table created successfully with table name 'components'.")
        except Error as e:
            print(f"Error creating table: {e}")

    def close_connection(self):
        """ close the database connection """
        if self.conn:
            self.conn.close()
            print(f"Connection to {self.db_file} closed.")
        else:
            print("No connection to close.")
    
    def fill_random_electronic(self, quantity):
        """ fill the database with random electronic components """
        query = "INSERT INTO components (name, serialID, category, sub_category, cabinet_ID, location, quantity, value) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        categories = ["Resistor", "Capacitor", "Inductor", "Diode", "Transistor"]
        sub_categories = ["Passive", "Active"]
        for i in range(quantity):
            name = f"Component_{i}"
            serialID = f"SERIAL_{i}"
            category = categories[i % len(categories)]
            sub_category = sub_categories[i % len(sub_categories)]
            cabinet_id = f"CABINET_{i // 10}"
            location = f"Location_{i}"
            quantity =  i
            value = f"Value_{i}"
            self.execute_query(query, (name, serialID, category, sub_category, cabinet_id, location, quantity, value))
            print(f"Inserted {name} into the database.")
            
    def execute_query(self, query, params=None):
        """ execute a single query """
        try:
            cursor = self.conn.cursor()
            if params:
                print(cursor.execute(query, params))
            else:
                print(cursor.execute(query))
            self.conn.commit()
            print("Query executed successfully.")
        except Error as e:
            print(f"Error executing query: {e}")
            self.conn.rollback()

    def search_all(self, query, params=None):
        """ fetch all results from a query """
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(f"Error fetching data: {e}")
            return None

    def search_component_by_cabinet(self, cabinet_id):
        """ fetch all components by cabinet ID """
        query = "SELECT * FROM components WHERE cabinet_ID = ?"
        params = (cabinet_id,)
        return self.search_all(query, params)
    
    def search_component_by_location(self, location):
        """ fetch all components by location """
        query = "SELECT * FROM components WHERE location = ?"
        params = (location,)
        return self.search_all(query, params)
    
    def search_component_by_name(self, name):
        """ fetch all components by name """
        query = "SELECT * FROM components WHERE name = ?"
        params = (name,)
        return self.search_all(query, params)
    
    def search_component_by_category(self, category):
        """ fetch all components by category """
        query = "SELECT * FROM components WHERE category = ?"
        params = (category,)
        return self.search_all(query, params)
    
    def search_component_by_sub_category(self, sub_category):
        """ fetch all components by sub category """
        query = "SELECT * FROM components WHERE sub_category = ?"
        params = (sub_category,)
        return self.search_all(query, params)  
    
    def search_component_by_category_and_sub_category(self, category, sub_category):
        """ fetch all components by category and sub category """
        query = "SELECT * FROM components WHERE category = ? AND sub_category = ?"
        params = (category, sub_category)
        return self.search_all(query, params)
    
    def search_componet_by_serialID(self, serialID):
        """ fetch all components by serial ID """
        query = "SELECT * FROM components WHERE serialID = ?"
        params = (serialID,)
        return self.search_all(query, params)
    
    def search_component_by_category_subcategory_and_value(self, category, sub_category, value):
        """ fetch all components by category, sub category and value """
        query = "SELECT * FROM components WHERE category = ? AND sub_category = ? AND value = ?"
        params = (category, sub_category, value)
        return self.search_all(query, params)
    
    def get_unique_categories(self):
        """ fetch all unique categories """
        query = "SELECT DISTINCT category FROM components"
        return self.search_all(query)
    
    def get_unique_sub_categories(self, category):
        """ fetch all unique sub categories """
        query = "SELECT DISTINCT sub_category FROM components WHERE category = ?"
        params = (category,)
        return self.search_all(query,params)
    
    def subtract_quantity(self, serialID, quantity):
        """ subtract quantity from a component """
        print(self.search_componet_by_serialID(serialID))
        query = "UPDATE components SET quantity = quantity - ? WHERE serialID = ?"
        params = (quantity, serialID)
        self.execute_query(query, params)
        print(self.search_componet_by_serialID(serialID))

    def isTableEmpty(self):
        """ check if the table is empty """
        query = "SELECT COUNT(*) FROM components"
        cursor = self.conn.cursor()
        cursor.execute(query)
        count = cursor.fetchone()[0]
        return count == 0
    
    def add_component(self, name, serialID, category, sub_category, cabinet_ID, location, quantity, value):
        """ add a component to the database """
        if self.search_componet_by_serialID(serialID) is not None:
            print(f"Component with serial ID {serialID} already exists.")
            raise ValidationError(f"Component with serial ID {serialID} already exists.")
            return
        query = "INSERT INTO components (name, serialID, category, sub_category, cabinet_ID, location, quantity, value) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        params = (name, serialID, category, sub_category, cabinet_ID, location, quantity, value)
        self.execute_query(query, params)
