from app import db
from app.models import Points, User, Bets
from app.helpers import up_rounds, fixture
from sqlalchemy import desc, func
from datetime import datetime
import pandas as pd
