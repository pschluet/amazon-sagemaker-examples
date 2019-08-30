FROM scikit

COPY extra-requirements.txt extra-requirements.txt
RUN pip install -r extra-requirements.txt

CMD jupyter lab --ip=0.0.0.0 --allow-root