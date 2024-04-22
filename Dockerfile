FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /code/

ENV USER temp

# create user
RUN useradd -ms /bin/bash ${USER}
USER ${USER}
WORKDIR /home/${USER}

# add aws credentials
RUN mkdir -p /home/${USER}/.aws
COPY aws/credentials /home/${USER}/.aws/credentials
COPY aws/config /home/${USER}/.aws/config

WORKDIR /code

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
