build_env:
	conda env create -f environment.yml
	conda activate surveyportal

build_docker:
	docker build -t streamlit .

run_docker:
	docker run -p 8501:8501 streamlit
