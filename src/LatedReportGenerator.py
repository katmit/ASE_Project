
data_sets = {"auto2.csv","auto93.csv","","","",""}
functs = {"all", "sway1", xpln1, sway2, xpln2, top} #what is top?

for data_set in data_sets:
    arr_results = {}





    data = None

    for x in range(20):

        data = Data(Common.config["file"])

        result = generate_stats(data_set)
        arr_results.append(result)



def generate_stats(data_set):
    results = {}

    print("\t\t\t" + data_set.getfirstlinelbls + "\n")

    for f in functs:
        result = f(data_set)
        print(f + "\t\t" + result + "\n")
        results.append(result)

    print("\n")
    print("\t\t\t" + data_set.getfirstlinelbls + "\n")

    for val in results("all"):
        for val2 in results("all"):
            if val == val2:
                print("=\t\t")
            else:
                print("!=\t\t")

    for val in results("all"):
        for val2 in results("sway1"):
            if val == val2:
                print("=\t\t")
            else:
                print("!=\t\t")

    for val in results("all"):
        for val2 in results("sway2"):
            if val == val2:
                print("=\t\t")
            else:
                print("!=\t\t")


    for val in results("sway1"):
        for val2 in results("sway2"):
            if val == val2:
                print("=\t\t")
            else:
                print("!=\t\t")

    for val in results("sway1"):
        for val2 in results("xpln1"):
            if val == val2:
                print("=\t\t")
            else:
                print("!=\t\t")


    for val in results("sway2"):
        for val2 in results("xpln2"):
            if val == val2:
                print("=\t\t")
            else:
                print("!=\t\t")


    for val in results("sway1"):
        for val2 in results("top"):
            if val == val2:
                print("=\t\t")
            else:
                print("!=\t\t")

    print("\n-------------------------------\n")

def run_sway1():
    for source in os.listdir(os.path.join(os.path.dirname(__file__), '../etc/data')):
        data = Data('../etc/data/' + source)
        sway_res = data.sway()
        print('all: ' + str(data.stats()))
        print('best: ' + str(sway_res['best'].stats()))
        print('rest: ' + str(sway_res['rest'].stats()))

        return results


def run_sway2():
    for source in os.listdir(os.path.join(os.path.dirname(__file__), '../etc/data')):
        data = Data('../etc/data/' + source)
        sway_res = data.sway()
        print('all: ' + str(data.stats()))
        print('best: ' + str(sway_res['best'].stats()))
        print('rest: ' + str(sway_res['rest'].stats()))

        return results


def run_sway1():
    for source in os.listdir(os.path.join(os.path.dirname(__file__), '../etc/data')):
        data = Data('../etc/data/' + source)
        sway_res = data.sway()
        print('all: ' + str(data.stats()))
        print('best: ' + str(sway_res['best'].stats()))
        print('rest: ' + str(sway_res['rest'].stats()))

        return results

def run_xpln1():

        for source in os.listdir(os.path.join(os.path.dirname(__file__), '../etc/data')):
            data = Data('../etc/data/' + source)
            sway_res = data.sway()
            xpln_res = data.xpln({'best': sway_res['best'], 'rest': sway_res['rest']})

            print('\n-----------\n')
            if xpln_res['rule'] != None:
                rule = xpln_res['rule']
                print('explain=' + str(show_rule(rule)))

                print('all               ' + str(data.stats("mid")) + ', ' + str(data.stats("div")))

                # TODO check if this is what we're actually supposed to do:
                data1 = data.clone(selects(rule, data.rows))
                print(
                    'sway with ' + str(sway_res['evals']) + ' evals ' + str(sway_res['best'].stats("mid")) + ', ' + str(
                        sway_res['best'].stats("div")))
                print('xpln on ' + str(sway_res['evals']) + ' evals   ' + str(data1.stats("mid")) + ', ' + str(
                    data1.stats("div")))

                top = data.betters(len(sway_res['best'].rows))
                top_data = data.clone(top[0])
                print('sort with ' + str(len(data.rows)) + ' evals   ' + str(top_data.stats("mid")) + ', ' + str(
                    top_data.stats("div")))

            print('\n-----------\n')

        return results


def run_xpln2():
    for source in os.listdir(os.path.join(os.path.dirname(__file__), '../etc/data')):
        data = Data('../etc/data/' + source)
        sway_res = data.sway()
        xpln_res = data.xpln({'best': sway_res['best'], 'rest': sway_res['rest']})

        print('\n-----------\n')
        if xpln_res['rule'] != None:
            rule = xpln_res['rule']
            print('explain=' + str(show_rule(rule)))

            print('all               ' + str(data.stats("mid")) + ', ' + str(data.stats("div")))

            # TODO check if this is what we're actually supposed to do:
            data1 = data.clone(selects(rule, data.rows))
            print(
                'sway with ' + str(sway_res['evals']) + ' evals ' + str(sway_res['best'].stats("mid")) + ', ' + str(
                    sway_res['best'].stats("div")))
            print('xpln on ' + str(sway_res['evals']) + ' evals   ' + str(data1.stats("mid")) + ', ' + str(
                data1.stats("div")))

            top = data.betters(len(sway_res['best'].rows))
            top_data = data.clone(top[0])
            print('sort with ' + str(len(data.rows)) + ' evals   ' + str(top_data.stats("mid")) + ', ' + str(
                top_data.stats("div")))

        print('\n-----------\n')

    return results







