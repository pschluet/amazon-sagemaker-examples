FROM jupyter/minimal-notebook

COPY extra-requirements.txt extra-requirements.txt
RUN pip install -r extra-requirements.txt

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt