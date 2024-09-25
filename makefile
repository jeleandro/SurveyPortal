conda env create -f environment.yml
conda activate surveyportal


docker build -t streamlit .
docker run -p 8501:8501 streamlit
