#!/bin/bash

nosetests -v -v --with-id --with-django --django-settings torch.settings --with-doctest --with-django-sqlite torch/
