# Terminal 1: Start the demo store
cd demo/store
pip install -r requirements.txt
python app.py
# Visit: http://localhost:80001

# Terminal 2: Start the delegation UI
cd demo/delegation-ui
pip install -r requirements.txt
python app.py
# Visit: http://localhost:80001
# To view the text narrative files created by the script:
cat public/narratives/adversarial_summary.json
# or check the local markdown files
cat docs/NARRATIVE_SYSTEM.md
kaggle kernels pull inversion/arc3-sample-submission-random-cd simulations

# Attack simulations
python attack_simulations.py               # Core attack simulation framework
python attack_track_fb.py                  # Trust manipulation attacks
python attack_track_fc.py                  # Economic attacks

# For full 4-Life game demos, see: https://github.com/dp-web4/4-life
