# image-web-service

I wanted to share some pictures I've taken while working with web services, so here we are!

## How to install

First, you will need to have a working [anaconda install](https://docs.anaconda.com/anaconda/install/).

Then clone the repository:

```
git clone https://github.com/tds325/image-web-service.git
```

Next inside the repository folder, initialize the anaconda environment:

```
conda env create --file=./environment.yml --prefix=<path>/<env_name>
conda activate <path>/<env_name>
```

image-web-service looks for images in the **`/srv/Pictures/`** directory, so you'll need to create one.

## Running image-web-service

Since image-web-service is a *Web Server Gateway Interface* application, you will need to deploy a **WSGI** server. There are several [options to choose from](https://werkzeug.palletsprojects.com/en/3.0.x/deployment/#self-hosted-options).

Here's what I used, and what I think is probably most simple:

```
conda install gunicorn
gunicorn image-get:application
```
This will spin up a localhost server on port 8000 where you can view the images that you stored within **`/srv/Pictures/`**.

To make this work over http(s), you will need to set up a reverse proxy server to communicate with gunicorn, such as [Apache2](https://httpd.apache.org/) or [nginx](https://nginx.org/).

## API Routes
`/`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-> get a random image from the directory

`/list`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-> list all image names in the directory

`/+`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-> get the metadata of a random image

`/<image_name>`&nbsp;&nbsp;&nbsp;&nbsp;-> fetch an image by name

`/<image_name>+`&nbsp;&nbsp;-> get the details of a specific image by name


## See it in action
## 
<http://ec2-100-27-40-16.compute-1.amazonaws.com/>

## Deployment

```
image-web-service
└── AWS EC2 Instance
    ├── nginx server (reverse proxy)
    ├── gunicorn WSGI server
    ├── miniconda
    │   ├── werkzeug
    │   ├── pillow
    │   └── pyexiftool
    └── exiftool
```
