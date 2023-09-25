"""Check the list of warnings produced by a doc build."""

import sys
from pathlib import Path

from colorama import Fore, init

# init colors for all plateforms
init()


def check_warnings(file: Path) -> bool:
    """Check the list of warnings produced by a doc build.

    Raise errors if there are unexpected ones and/or if some are missing.

    Parameters:
        file: the path to the generated warning.txt file from
            the CI build

    Returns:
        0 if the warnings are all there
        1 if some warning are not registered or unexpected
    """
    # print some log
    print("\n=== Sphinx Warnings test ===\n")

    # find the file where all the known warnings are stored
    warning_file = Path(__file__).parent.parent / "warning_list.txt"

    test_warnings = file.read_text().strip().split("\n")
    ref_warnings = warning_file.read_text().strip().split("\n")

    print(
        f'Checking build warnings in file: "{file}" and comparing to expected '
        f'warnings defined in "{warning_file}"\n\n'
    )

    # find all the missing warnings
    missing_warnings = []
    for wa in ref_warnings:
        if index := [i for i, twa in enumerate(test_warnings) if wa in twa]:
            test_warnings.pop(index[0])

        else:
            missing_warnings += [wa]
            print(f"{Fore.YELLOW}Warning was not raised: {Fore.RESET}{wa}\n")
    # the remaining one are unexpected
    for twa in test_warnings:
        print(f"{Fore.YELLOW}Unexpected warning: {Fore.RESET}{twa}\n")

    return len(missing_warnings) != 0 or len(test_warnings) != 0


if __name__ == "__main__":
    # cast the file to path and resolve to an absolute one
    file = Path.cwd() / "warnings.txt"

    # execute the test
    sys.exit(check_warnings(file))
