import os
import sys
import subprocess
from tqdm import tqdm

for problem_id in sys.argv[1:]:

	os.chdir('problems')
	os.chdir(problem_id)
	os.system('> output_input.txt')

	pwd_list = sorted(os.listdir())
	
	test_str = "test_input_" + problem_id + ".py"

	for i, solution_filename in enumerate(tqdm(pwd_list)):

		if 'solution_' not in solution_filename:	
			continue

		# extract solution id
		solution_id = solution_filename[9:-3]

		import_str = "solution_" + solution_id
		cmd = f"pytest {test_str} --tb=line --solution {import_str} --timeout=2"
		# os.system(cmd + " >> output_input.txt")

		# separate test results from the command output
		try:
			output_str = subprocess.check_output(cmd, shell=True).decode('utf-8')
			result = output_str.split("\n")[9]
			result = result.split(" ")[1]

		except Exception as e:
			#print(f"ERROR {solution_id}:", e.output.decode('utf-8'))

			e_str = str(e)[-2]

			if e_str == '1':
				output_str = e.output.decode('utf-8')
				result = output_str.split("\n")[9]
				result = result.split(" ")[1]
			elif e_str == '2':
				result = "ERROR"
			else:
				result = "UNKNOWN EXIT STATUS"
				
		os.system(f"echo '{solution_id} {result}'>>output_input.txt")


	os.chdir('..')
