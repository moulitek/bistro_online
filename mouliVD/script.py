from operator import sub
from moulitek.moulitek import *
import subprocess
import json
import os

buffer = open("./tests.json")

inside = buffer.read()

test_dict = json.loads(inside)

for category in test_dict:
    new_category = Category(category["name"], category["desc"])
    for sequences in category["sequences"]:
        seq = new_category.add_sequence(sequences["name"], sequences["desc"])
        for test in sequences["tests"]:
            seq.add_test(test["name"], test["desc"])
            passed = None
            reason = None
            expected = None
            got = None
            output = call_system(test["test"], timeout=60)
            if output == test["ret"]:
                os.system(test["test"] + " > testing")
                inside = open("./testing")
                out = inside.read()
                inside.close()
                os.system("rm testing")
                if out == test["exp"]:
                    passed = True
                else:
                    passed = False
                    reason = BADOUTPUT
                    expected = str(test["exp"])
                    got = str(out)
            elif output == 127:
                reason = TIMEOUT
                passed = False
                expected = str(test["ret"])
                got = str(output)
            elif output == 139 or output == 136:
                passed = False
                reason = SEGFAULT
                expected = str(test["ret"])
                got = str(output)
            else:
                passed = False
                reason = RETVALUE
                expected = str(test["ret"])
                got = str(output)
            seq.set_status(test["name"], passed=passed, reason=reason, expected=expected, got=got)

gen_trace()

SEGFAULT | BADOUTPUT | RETVALUE | TIMEOUT

buffer.close()
