# generate_submit_scripts.py

num_scenarios = 50

for scenario_id in range(num_scenarios):
    with open(f'submit_job_{scenario_id}.sh', 'w') as f:
        script_content = open('submit_job_template.sh').read()
        f.write(script_content % (scenario_id, scenario_id, scenario_id, scenario_id))
