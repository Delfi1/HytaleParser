### To use the script install all dependencies with 

```powershell
pip install -r “requirements.txt”
```

### And then run main.py (default args):
```powershell
python main.py --main True --media True 
```
#### The “--main” flag is needed to parse the main pots.
#### Flag “--fanarts” to parse posts with fan-arts.
#### The “--media” flag for installing from the /media tab
#### The "--posts" flag. Overrides "--main" and "--fanarts". Example: "[0, 1, 51]"