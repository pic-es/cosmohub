[![Build Status](https://travis-ci.com/pic-es/cosmohub.svg?branch=master)](https://travis-ci.com/pic-es/cosmohub)
[![codecov](https://codecov.io/gh/pic-es/cosmohub/branch/master/graph/badge.svg)](https://codecov.io/gh/pic-es/cosmohub)
[![codebeat badge](https://codebeat.co/badges/689d424c-b496-4a82-aa07-313a4f394e7b)](https://codebeat.co/projects/github-com-pic-es-cosmohub-master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3cf43c848e6241cb8fdd703c2eafeeff)](https://www.codacy.com/gh/pic-es/cosmohub?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=pic-es/cosmohub&amp;utm_campaign=Badge_Grade)

Per reordenar els imports:

    find cosmohub -type f -name \*.py -exec pipenv run reorder-python-imports {} \;

Per reformatar el codi font:

    pipenv run black -l 120 -t py36 .

Per inicialitzar la base de dades:

    cd cosmohub && FLASK_ENV=<env> pipenv run flask db upgrade && cd ..

Per executar en mode de depuració:

    FLASK_APP=cosmohub/app.py FLASK_DEBUG=1 pipenv run flask run

Per córrer el conjunt de proves:

    pipenv run coverage run --source=cosmohub -m pytest

Per generar l'informe de cobertura:

    pipenv run coverage report -m

