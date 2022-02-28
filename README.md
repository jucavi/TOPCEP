# Online Test Python Institude

[Python Institute](https://pythoninstitute.org/certification/pcep-certification-entry-level/pcep-exam-syllabus/)

## Usage

1. Clone repository
``` bash
$ git clone https://github.com/jucavi/TOPCEP.git
$ cd TOPCEP
```

2. Create virtual environemnt
``` bash
$ python3 -m venv .venv
$ source .venv/bin/activate
```

3. Install requirements
``` bash
$ pip3 install -r requirements.txt
```

4. Create .env
``` bash
$ nano .env
```

5. Edit .env
```
FLASK_APP=main.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

6. Make sure you have pcep.json file in TOPCEP directory with this structure:
```json
{
    "BLOCK_EXAMPLE": [
        {
            "question": "some question",
            "options": [
                "option 1", # Correct
                "option 2",
                "option 3"
            ],
            "answer": 0 # Index of correct answer
        },
        {
            ...
        }
    ],
    "OTHER BLOCK": [
        {
            "question": "some other question",
            "options": [
                "option 1",
                "option 2", # Correct
                "option 3"
            ],
            "answer": 1 # Index of correct answer
        },
        {
            ...
        }
    ]
}
```

7. Populate database
```bash
$ python3 question_seeds.py
```

8. Run server
```
$ flask run
```