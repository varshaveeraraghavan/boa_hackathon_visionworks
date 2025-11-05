# Steps to run:
## Create a virtual environment named "api-sim"
conda create -n api-sim python=3.10 -y

## Activate the environment
conda activate api-sim

## Open terminal and execute the following commands
cd backend
pip install -r requirements.txt
uvicorn app:app --reload

## Open another terminal and execute the following commands
cd frontend
npm install
npm start
