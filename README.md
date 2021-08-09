# SA_visualiser
This is an interactive tool that allows to visualise the price of the agricultural products in the different  marketplaces in colombia. The information is taking from the [SIPSA](https://www.dane.gov.co/index.php/servicios-al-ciudadano/servicios-informacion/sipsa)  which is the plataform managed by Colombian Department for Statistics [DANE](https://www.dane.gov.co/) (Departamento Administrativo Nacional de Estadística DANE)

The file [Procfile](https://raw.githubusercontent.com/endorgobio/SA_visualiser/master/Procfile) specifies the commands that are executed by the app on startup. You can use a Procfile to declare a variety of process types, including Your app’s web server. [details](https://devcenter.heroku.com/articles/procfile)

The file [runtime](https://raw.githubusercontent.com/endorgobio/SA_visualiser/master/runtime.txt) specifies the python version to be run.

The file [requirements.txt](https://raw.githubusercontent.com/endorgobio/SA_visualiser/master/requirements.txt) provides the dependencies to be installed

The data is update daily using a [workflow](https://docs.github.com/es/actions/learn-github-actions) in github. The file in [update_data.yml](https://raw.githubusercontent.com/endorgobio/SA_visualiser/31c89961f1f4aff444fe2af3a51de96fd954951c/.github/workflows/update_data.yml) provides the details. It runs a python script with its own dependencies ([requerimentsGH.txt](https://raw.githubusercontent.com/endorgobio/SA_visualiser/master/requerimentsGH.txt)) that are installed when the action in the workflof is carried on

The user interface/dashboard is developed in Dash. A running version of it is avaibale at [https://savisualiser.herokuapp.com/](https://savisualiser.herokuapp.com/)
