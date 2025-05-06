from flask import Flask, jsonify, render_template
import requests  
from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine, insert,MetaData,Table,Column,Integer,String,REAL


app = Flask(__name__)


metadata_obj = MetaData()

weather_table =Table(
    "weather_data",
    metadata_obj,
    Column("cidade", String(255)),
    Column("lon", REAL),
    Column("lat", REAL),
    Column("clima", String(255)),
    Column("umidade", REAL),
    Column("temperatura", REAL),
)

