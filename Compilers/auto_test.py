import os
import sys
import subprocess
import re
import json
#from subprocess import PIPE



def test_main(person,DIR,language,args,compile_args):
    
    size_test = (len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])) //2
    src_file = "src/{!s}".format(person)

    report = "Aluno: {!s}\n \n".format(person)

    failed_test = False

    args.append("")

    if language != "python3": #refatorar esse codigo, dois checks iguais
        output = compile(src_file,compile_args)

        if output: #strings vazias são falsas
            report += "Error: teste automatico não conseguio compilar arquivo!\n"
            report += "parametros de compilação: {!s}\n".format(" ".join(compile_args))
            report +=  "erro de compilação:{!s}".format(output)
            report_writer(report,person)
            return True

    for i in range(1,size_test + 1):
        test_file = DIR +"/teste{!s}.txt".format(i)
        sol_file = DIR +"/sol{!s}.txt".format(i)

        data = get_text(test_file)
        args[-1] = data
        #data_encoded = str.encode(data)

        output = get_program_output(src_file,language,args)

        if output == "":
            report += "Error: main file not found\n"
            report_writer(report,person)
            #print(output)
            return True

        sol = get_text(sol_file)
        sol = text_processor(sol)

        try: #fazer esse try melhor
            first_digit = re.search(r"\d", output) #lida com texto aleatorio das versão 1.0
            first_digit = first_digit.start()
        except: #tratar o erro do mesmo jeito que o outro
            report += "teste{!s}: falha\n".format(str(i))
            report += "output esperado: {!s} | output recebido:{!s}\n \n".format(str(sol),str(output))
            failed_test = True
            continue

        if output[first_digit-1] == "-": # não sei se tem jeito melhor que esse
            first_digit -= 1 # feito para não ignorar numeros negativos

        output = output[first_digit:]
        output = text_processor(output)

        result = assertEquals(sol, output)
        if result:
            report += "teste{!s}: ok\n \n".format(str(i))
        else:
            report += "teste{!s}: falha\n".format(str(i))
            report += "input do teste: {!s} ".format(str(data))
            report += "output esperado: {!s} | output recebido:{!s}\n \n".format(str(sol),str(output))
            failed_test = True

    if failed_test:
        report_writer(report,person)

    return failed_test

def assertEquals(var1, var2):
    return var1 == var2

def get_text(test_file):
    with open(test_file, 'r') as file:
        data = file.read()
    return data

def get_program_output(src_file,language,args):
    #if language =="python3":
    #    args = ["python3",src_file,data]

    output = subprocess.run(args,cwd=src_file,stderr=subprocess.PIPE,stdout=subprocess.PIPE)

    text = output.stdout.decode("utf-8")
    text = text_processor(text)

    return text

def compile(src_file,compile_args):
    output = subprocess.run(args,cwd=src_file,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    text = output.stderr.decode("utf-8")

    return text

def text_processor(text):
    text = os.linesep.join([s for s in text.splitlines() if s])
    text.strip()

    return text

def report_writer(report,person):
    person_file = "reports/{!s}.txt".format(person)
    with open(person_file, 'w') as file:
        file.write(report)


def read_git_url_json():
    with open("git_paths.json") as git_urls:
        return json.load(git_urls)


if __name__ == '__main__':
    test_dir = "tests/{!s}_tests".format(sys.argv[1])
    acepeted_languages = ["python3","C++"]

    json_file = read_git_url_json()


    for student in json_file:
        p = student["student_username"]
        language = student["language"]
        args = student["run_args"]
        args = args.split()
        compile_args = ""
        
        if (language not in acepeted_languages):
            raise Exception("language {!s} is not a acepeted language!".format(language))

        if (language != "python3"): # pegar argumento de compilação
            compile_args = student["compile_args"]
            compile_args = compile_args.split()
            compile_args.append("-w") #supress warnings
        
        if (not os.path.exists("reports/{!s}.txt".format(p))):
            print(p)
            error = test_main(p,test_dir,language,args,compile_args)
            print("algum erro?: ",error)