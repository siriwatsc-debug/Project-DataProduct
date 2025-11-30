import pandas as pd
import numpy as np
import re


url = 'https://github.com/siriwatsc-debug/Project-DataProduct/raw/refs/heads/main/Dataset/AllDataset_Edit_Final_R04.xlsx'


# ชื่อโรค $ label column : ชื่อ sheet ที่ต้องการ train
target_dataframes = {
    'Diabetes $ label': '2.diabetes_prediction_dataset(เ',
    'Obesity $ Label': '5.ObesityDataSet_raw_and_data_s',
    'Liver $ Label': '6.liver_data_with_metadata(ตับ)',
    'Kidney $ Label1': '8.kidney_disease_dataset(ไต)',
    'Kidney $ Label2': '8.kidney_disease_dataset(ไต)',
}

sh_data_dic = 'Data Dic (Not Duplicate Item)'



excel_df = pd.read_excel(url, sheet_name=None, header=None)

list_sheet = list(excel_df.keys())
print(list_sheet)


df_for_st = excel_df[sh_data_dic]
# set header row1 for df_for_st, drop row 1
df_for_st.columns = df_for_st.iloc[0]
df_for_st = df_for_st[1:]

# create new column Value_Clean refer column "Value" convert str to list # split by newline or comma # ignore nan float
df_for_st['Value_Clean'] = df_for_st['Value'].apply(
    lambda x: re.split(r'\n|,', str(x)) if isinstance(x, str) else []
)

# create new dictionay "field name" as key, Value_Clean as value
dict_st = df_for_st.set_index('field name')['Value_Clean'].to_dict()
print(dict_st)



all_data = {}
for key in target_dataframes:
    sh = target_dataframes[key]
    sp = key.split(' $ ')
    label_col = sp[1]
    print()
    print( '*** check sheet', sh )
    df = excel_df[sh].copy()

    column_st = df.loc[1]
    df = df.iloc[3:]
    df.columns = column_st
    all_data[key] = df.copy()
    if( label_col not in df.columns ):
      print('>>>>>>>>>> label_col error', df.columns)

    # filter column start with st_
    column_st = [c for c in column_st if c.startswith('st_')]
    # unique value of column_st
    unique_values = df[column_st].apply(lambda x: x.unique())

    for col, uq_val in unique_values.items():
        print('check col', col)
        for uq in uq_val:
          if( uq not in dict_st[col] and uq is not np.nan ):
            print('------ value not found in ST sheet', col, uq)

list_features = {}
for key in target_dataframes:
  list_features[key] = [c for c in all_data[key].columns if c.startswith("lv_") or c.startswith("st_")]
print(list_features)
# -------------------------- end checking












# =========================== TRAIN
print('*** TRAIN ***')

import json
import os

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from imblearn.over_sampling import RandomOverSampler
from imblearn.pipeline import Pipeline as ImbPipeline

from sklearn.preprocessing import label_binarize
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


# -----------------------------
# Function for Training + Predict with balancing
# -----------------------------
def train_and_predict_balanced(df, label_col="label", test_size=0.2, random_state=42):
    # --- Select columns
    _df_train = df.copy()
    _df_train = _df_train[[c for c in df.columns if c.startswith("lv_") or c.startswith("st_")] + [label_col]].copy()
    _df_train.columns = [c for c in df.columns if c.startswith("lv_") or c.startswith("st_")] + ['label']
    
    X = _df_train.drop('label', axis=1).copy()
    y = _df_train['label'].copy()

    # --- Encode label
    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    # --- Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=test_size, random_state=random_state, stratify=y_enc
    )

    # --- Separate columns
    lv_cols = [c for c in X.columns if c.startswith("lv_")]
    st_cols = [c for c in X.columns if c.startswith("st_")]

    # --- Preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ("scale_lv", StandardScaler(), lv_cols),
            ("encode_st", OneHotEncoder(handle_unknown="ignore"), st_cols)
        ],
        remainder="drop"
    )

    # --- Oversampler
    ros = RandomOverSampler(random_state=42)

    # --- Pipeline with imbalance handling
    num_class = len(np.unique(y_enc))
    pipeline = ImbPipeline([
        ("preprocessor", preprocessor),
        ("oversample", ros),
        ("model", XGBClassifier(
            objective="multi:softmax",
            eval_metric="mlogloss",
            num_class=num_class,
            random_state=42
        ))
    ])

    # --- Train
    pipeline.fit(X_train, y_train)

    # --- Predict
    y_pred = pipeline.predict(X_test)  # array([1])

    # --- Scores
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted")
    recall = recall_score(y_test, y_pred, average="weighted")
    f1 = f1_score(y_test, y_pred, average="weighted")

    # y_prob = pipeline.predict_proba(X_test)                  # array([[0.3, 0.7]]) for example
    # y_test_bin = label_binarize(y_test, classes=np.arange(num_class))
    # print(num_class, y_test, y_test_bin)
    # auc = roc_auc_score(
    #     y_test_bin, y_prob, multi_class="ovr", average="weighted"
    # )

    # --- Return
    scores = {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1-Score": f1,
        # "AUC-Score": auc
    }

    # --- Return pipeline + label encoder
    return pipeline, le, scores, _df_train


import joblib
import os # For managing file paths


def save_pipeline(pipeline, file_path):
    with open(file_path, 'wb') as file:
        joblib.dump(pipeline, file)

def save_le(le, file_path):
    with open(file_path, 'wb') as file:
        joblib.dump(le, file)



# absolute path
model_dir = os.path.join(os.path.dirname(__file__), 'Models')

# delete all file in Models
for filename in os.listdir(model_dir):
    os.remove(os.path.join(model_dir, filename))




file_path = os.path.join(model_dir, 'list_features.json')
with open(file_path, 'w') as f:
    json.dump(list_features, f, indent=4)

print(f"'list_features' saved to {file_path}")








all_pipelines = {}
df_score = []
for i, k in enumerate(all_data):
    # if i == 1:
    #   continue
    sp = k.split(' $ ')
    label = sp[1]
    print(i, k)

    df = all_data[k].copy()
    
    print(df.columns)
    pipeline, le, score, df_train = train_and_predict_balanced(df, label)
    all_pipelines[k] = {
        'pipeline': pipeline,
        'le': le,
    }

    csv_path = os.path.join(model_dir, f"original_{k}.csv")
    df_train.to_csv(csv_path, index=False)

    filename_prefix = k
    pipeline_filename = f'{filename_prefix}$$pipeline.joblib'
    le_filename = f'{filename_prefix}$$le.joblib'
    save_pipeline(pipeline, os.path.join(model_dir, pipeline_filename))
    save_le(le, os.path.join(model_dir, le_filename))

    data_score = {}
    data_score['key $ label'] = k
    data_score = data_score | score
    df_score.append(data_score)


print(pd.DataFrame(df_score))