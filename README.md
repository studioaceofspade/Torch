Torch
=====

It's awesome, you wouldn't even know.

Installing
==========

    sudo apt-get install libpq-dev python-dev  # Needed for psycopg2
    virtualenv --distribute torch
    source torch/bin/active
    cd Torch
    ./install_all_reqs.sh
    echo `pwd` > ../torch/lib/python2.7/site-pachages/torch.pth
    ./run_test.sh
