import os
import joblib

import re
import json
from typing import Dict, Tuple


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import bcrypt

from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
import pandas as pd
import duckdb



class MyMongoDB():
    def __init__(self, uri):
        self.collection = {}
        
        # Create a new client and connect to the server
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        # client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=False, tlsCAFile=certifi.where())

        self.is_connect = False
        # Send a ping to confirm a successful connection
        try:
            self.client.admin.command('ping')
            self.is_connect = True

            self.init_db()
            self.read_collection('users')

            self.insert_user('user123', 'password123')

        except Exception as e:
            print(e)
            
    
    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()  # เก็บเป็น string ใน MongoDB

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    def init_db(self):
        self.db = self.client['project_db']
    
    def read_collection(self, _collection):
        self.collection[_collection] = self.db[_collection]

    def login(self, username, password):
        user = self.collection['users'].find_one({"username": username})
        if not user:
            return False

        if self.verify_password(password, user["password"]):
            # print(user)
            return user['_id']
        return None

    def register(self, username, password):
        user = self.collection['users'].find_one({"username": username})
        if user:
            return False

        self.insert_user(username, password)
        return True

    def select_user_info(self, username):
        user = self.collection['users'].find_one({"username": username})
        return user
    
    def select_user_health_data(self, username, options):
        self.read_collection('user_health_data')
        df_user_health_data = pd.DataFrame(
            self.collection['user_health_data'].find({"username": username}).to_list()
        )
        if df_user_health_data.empty:
            return []

        query = ''

        filter_year = ''
        if options.get('filters', None) != None:
            if options['filters'].get('year', None) != None:
                filter_year = f"and YEAR(CAST(date AS DATE)) = {options['filters']['year']}"
        
        select_columns = ''
        option_columns = options.get('columns', [])
        if len(option_columns) > 0:
            for col in option_columns:
                select_columns += f", health_data->>'{col}' as '{col}'"
        else:
            df_user_health_data['health_data'] = df_user_health_data['health_data'].apply(
                lambda x: json.dumps(x)
            )
            select_columns = ', health_data as str_health_data'

        query += f"SELECT date {select_columns} from df_user_health_data where 1=1 {filter_year} order by date"
        # print(query)
        result = duckdb.query(query).to_df().to_dict(orient="records")
        return result
    
    def delete_user_health_data(self, data):
        username = data['username']
        date = data['date']
        self.read_collection('user_health_data')
        self.collection['user_health_data'].delete_one({"username": username, "date": date})
        return True
    
    def insert_user_health_data(self, data):
        username = data['username']
        date = data['date']
        data.pop('username')
        data.pop('date')

        user = {
            "username": username,
            "date": date,
            "health_data": data
        }
        self.read_collection('user_health_data')
        
        self.collection['user_health_data'].update_one(
            {"username": username, "date": date},   # filter
            {
                "$set": {                           # อัปเดตทุกครั้ง
                    "health_data": data
                },
                "$setOnInsert": {                   # ตั้งครั้งแรกเท่านั้น
                    "username": username,
                    "date": date
                }
            },
            upsert=True
        )

    def insert_user(self, username, raw_password, user_info=None):
        user = {
            "username": username,
            "password": self.hash_password(raw_password),
            "user_info": user_info
        }

        self.collection['users'].update_one(
            {"username": username},           # filter
            {
                "$set": {                     # update ทุกครั้ง
                    "password": user["password"],
                    "user_info": user["user_info"]
                },
                "$setOnInsert": {             # set เฉพาะตอน insert
                    "username": username
                }
            },
            upsert=True
        )

    def create_collection_from_df(self, collection_name, df):
        # 1) ลบ collection เดิม
        if collection_name in self.db.list_collection_names():
            self.db.drop_collection(collection_name)

        # 2) สร้าง collection ใหม่
        self.read_collection(collection_name)

        # 3) Convert DataFrame → list of dict
        records = df.to_dict(orient="records")

        # 4) Insert all
        if len(records) > 0:
            self.collection[collection_name].insert_many(records)

        return True




from google import genai
from google.genai import types
# import google.generativeai as genai

class MyAIGenerator:
    def __init__(self, google_api_key, model_name):
        self.client = genai.Client(api_key=google_api_key)
        self.model = model_name

        self.json_schema = {
            "type": "object",
            "required": ["overall_recommendation", "desease_risk"],
            "properties": {
                "overall_recommendation": {
                    "type": "array",
                    "description": "แนะนำ การดูแลสุขภาพ เรียงลำดับความสำคัญจาก 1-5",
                    "items": {
                        "type": "string",
                        "description": "การดูแลสุขภาพที่เหมาะสม"
                    }
                },
                "desease_risk": {
                    "type": "array",
                    "description": "โรคที่มีความเสี่ยง",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "ชื่อโรค"
                            },
                            "risk": {
                                "type": "string",
                                "description": "ระดับความเสี่ยง"
                            },
                            "recommendation": {
                                "type": "string",
                                "description": "แนะนำ การดูแลสุขภาพ"
                            }
                        },
                        "required": ["name", "risk", "recommendation"]
                    },
                }
            },
        }
        self._read_template()

    def get_response(self, input_data):
        input_json_string = self._generate_json_string_with_full_comments(input_data)
        prompt = self.template_prompt.replace('{{input_json_string}}', input_json_string)
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=self.json_schema
            )
        )

        raw = response.text

        # 1) ลบ ```json และ ```
        clean = re.sub(r"```json|```", "", raw).strip()
        # 2) แปลงเป็น dict
        result_dict = json.loads(clean)

        return result_dict
    
    def _parse_data_structure(self, json_string: str) -> Dict[str, Tuple[str, str, int]]:
        """Parses a JSON-like string with embedded comments and group headers."""
        structure_map = {}
        current_group_text = None
        current_group_num = None
        
        header_pattern = re.compile(r'^\s*#\s*(\d+)\.\s*(.*)')
        key_comment_pattern = re.compile(r'\s*"(.*?)"\s*:\s*.*?\s*#\s*(.*)')

        for line in json_string.split('\n'):
            header_match = header_pattern.match(line)
            if header_match:
                current_group_num = int(header_match.group(1))
                current_group_text = header_match.group(2).strip()
                continue
                
            key_comment_match = key_comment_pattern.search(line)
            if key_comment_match and current_group_text and current_group_num:
                original_key = key_comment_match.group(1).strip()
                description = key_comment_match.group(2).strip()
                
                structure_map[original_key] = (description, current_group_text, current_group_num)

        return structure_map

    def _format_value(self, value) -> str:
        """Ensures None is printed as 'None' and strings are quoted."""
        if value is None:
            return 'None'
        # Use json.dumps for safe representation of strings/numbers/bools
        return json.dumps(value)

    def _generate_json_string_with_full_comments(self, input_data: dict) -> str:
        """
        Formats a dictionary into a JSON-like string, including all known keys 
        (defaulting to None if missing) and placing unknown keys in a new last group.
        """
        # 1. Separate known keys from unknown keys
        known_keys = [k for k in self.comment_map.keys()]
        unknown_keys = sorted([k for k in input_data.keys() if k not in known_keys])
        
        # 2. Prepare the list of keys to process (known keys sorted, followed by unknown keys)
        # Sorting known keys by group number
        known_keys_sorted = sorted(known_keys, key=lambda k: self.comment_map[k][2])
        
        output_lines = ['input_data = {']
        current_group = None
        
        # 3. Define metadata for the UNKNOWN group
        UNKNOWN_GROUP_NUM = 99
        UNKNOWN_GROUP_TEXT = 'ข้อมูลเพิ่มเติมที่ไม่อยู่ในโครงสร้างหลัก (Additional Data)'
        
        # 4. Process all known keys
        for key in known_keys_sorted:
            value = input_data.get(key, None) 
            comment, group_text, group_num = self.comment_map[key]
            
            # Add group header
            if group_text != current_group:
                if current_group is not None:
                    output_lines.append('')
                    
                header_line = f'    # {group_num}. {group_text}'
                output_lines.append(header_line)
                current_group = group_text

            # Format and append the line
            value_str = self._format_value(value) 
            line_prefix = f'    "{key}": {value_str},'
            output_lines.append(f'{line_prefix:<35} # {comment}')

        # 5. Process UNKNOWN keys if any exist
        if unknown_keys:
            output_lines.append('')
            
            # Add UNKNOWN group header
            header_line = f'    # {UNKNOWN_GROUP_NUM}. {UNKNOWN_GROUP_TEXT}'
            output_lines.append(header_line)
            
            # Process unknown keys
            for key in unknown_keys:
                value = input_data[key]
                value_str = self._format_value(value) 
                line_prefix = f'    "{key}": {value_str},'
                
                # Use a generic comment for unknown keys
                output_lines.append(f'{line_prefix:<35} # Key is not in the original structure')

        output_lines.append('}')
        return '\n'.join(output_lines)
        
    def _read_template(self):
        f = os.path.join(os.path.dirname(__file__), 'template_prompt.txt')
        with open(f, 'r', encoding='utf-8') as f:
            self.template_prompt = f.read()
        f = os.path.join(os.path.dirname(__file__), 'template_input_data.txt')
        with open(f, 'r', encoding='utf-8') as f:
            self.template_input_data = f.read()
        self.comment_map = self._parse_data_structure(self.template_input_data)





class MyModel:
    def __init__(self):
        self.model_dir = os.path.join(os.path.dirname(__file__), 'Models')
        self.loaded_list_features = None
        self.loaded_pipelines = {}
        
        self._load_model_and_feature()

        pass
    
    def _load_model_and_feature(self):
        model_dir = self.model_dir
        for filename in os.listdir(model_dir):
            if filename == 'list_features.json':
                with open(os.path.join(model_dir, filename), 'r') as f:
                    self.loaded_list_features = json.load(f)
                    print(f"Loaded list_features")
                continue

            if filename.endswith('$$pipeline.joblib'):
                key = filename.replace('$$pipeline.joblib', '')
                pipeline_path = os.path.join(model_dir, filename)
                le_path = os.path.join(model_dir, f'{key}$$le.joblib')

                if os.path.exists(le_path):
                    pipeline = self._load_pipeline(pipeline_path)
                    le = self._load_le(le_path)
                    self.loaded_pipelines[key] = {
                        'pipeline': pipeline,
                        'le': le,
                    }
                    print(f"Loaded model: {key}")
                else:
                    print(f"Warning: Missing label encoder for {key}. Skipping.")

    def _load_pipeline(self, file_path):
        with open(file_path, 'rb') as file:
            return joblib.load(file)
            
    def _load_le(self, file_path):
        with open(file_path, 'rb') as file:
            return joblib.load(file)

    def _get_dict_feature(self, list_features, input_data):
        model_input_dicts = {}

        for model_name, features in list_features.items():
            model_data = {}
            for feature in features:
                model_data[feature] = input_data.get(feature, None)
            model_input_dicts[model_name] = model_data

        result = {}
        for model_name, data in model_input_dicts.items():
            result[model_name] = data

        return result
    
    def predict_all_models(self, _input_data):
        input_dict = self._get_dict_feature(self.loaded_list_features, _input_data)

        all_predict = {}
        for key in self.loaded_pipelines:
            data = [input_dict[key].values()]
            
            original_df = pd.read_csv(os.path.join(self.model_dir, f'original_{key}.csv'))

            df_new = pd.DataFrame(data, columns=self.loaded_list_features[key])

            # full pipeline stored in 'model'
            pipeline = self.loaded_pipelines[key]['pipeline']
            le = self.loaded_pipelines[key]['le']

            # Predict class labels (1D array)
            y_pred_new = le.inverse_transform(pipeline.predict(df_new))  # array([1])
            y_prob_new = pipeline.predict_proba(df_new)                  # array([[0.3, 0.7]]) for example

            # print(key, "y_pred_new:", y_pred_new)
            # print(key, "y_prob_new:", y_prob_new)
            all_predict[key] = {
                'predict': y_pred_new[0],
                'probability': y_prob_new[0].max(),
                'prob': y_prob_new[0],
                'feature_input': input_dict[key],
                'original_df': original_df
            }
        return all_predict

