## O2 Web Hosting Report (2024)

By Doug Feldmann, HMS IT DevOps

### History and Background

Orchestra web hosting was one of the first options for Linux web hosting at HMS.  It quickly became a popular way to host any kind of website, from static HTML and raw data sharing sites to PHP and CGI web applications.  Many of these sites were specialized research tools, using resources provided by Research Computing (including the HPC cluster).  But many were not.  It was easy to install a CMS like Wordpress on Orchestra and many labs had simple brochure sites.  The Countway Library site was deployed on Orchestra Web as were many Harvard Catalyst tools and resources.  Harvard Health Publishing also used Orchestra Web.

By the late 2010s, Research Computing was trying to realign the web hosting service to be more research-focused.  Countway, Catalyst, and Harvard Health all migrated to other infrastructure.  New site creation was discouraged and users were encouraged to use alternatives such as OpenScholar instead.  Multiple events over the next few years led to an increased migration of sites off RC's Web Hosting.  Many brochure sites were consolidated into the HMS-wide Drupal service while others were identified and decommissioned.  A dedicated project was undertaken to survey and relocate sites.  The original Orchestra Web hosting cluster was migrated to the current O2 Web Hosting in 2020, and several more sites were migrated away.

In aggregate, these efforts were largely successful in the stated goal of reducing the scope of Research Computing's web hosting service.  As of 2024, there's only one pure Wordpress site still hosted by Research Computing on O2 Web Hosting (mghbwhid.hms.harvard.edu) and fewer than five static brochure sites remain.  Ironically, the two sites RC was most particularly eager to migrate (pathcore.hms.harvard.edu and nhpdata.med.harvard.edu) remain on O2 Web Hosting.  Regardless, more than two-thirds of the sites remaining on O2 Web Hosting are nominally research-related and more than half are clearly some sort of specialized tool or data browser.

### Current Usage Profile

After the policy changes, the typical O2 Web site would be difficult, awkward or even impossible to host on a SaaS, requiring PaaS such as Heroku or general purpose web hosting.  Some of these sites do rely on HPC resources, either compute or storage, but many are simply custom web-based applications that don't fit well into the Wordpress/Drupal model.  Once allocated a site, O2 Web developers have substantial freedom to deploy custom software, contacting HMS IT only if they need specific php extensions enabled or operating system packages installed.

As a consequence, it's somewhat difficult to generalize about the service.  Many sites on O2 were deployed before the expansion of the PMO, either as informal projects or as request tickets, during an era of more lax security standards.  Users vary widely.  Some sites are maintained by full-time developers while others are developed up by a postdocs or grad students before handing them over to the lab for ad hoc maintenance.  Still others hire contractors on a project basis leaving long-term maintenance responsibility ambiguous.

### Service Components

There are several components to the O2 Web Hosting environment.  Most are optional for a given site.

#### HTTP/S Ingress with SSL Termination and Loadbalancing.

O2Web maintains both public-facing and internal-facing HAProxy loadbalancers.  HAProxy is a These are integrated with the other web components but can also be configured to serve as an ingress and loadbalancer for any type of web service.  Sample sites that use only the loadbalancer but are otherwise standalone services are eLab Journal (elab.hms.harvard.edu) and the O2 Portal (o2portal.rc.hms.harvard.edu).

#### Apache HTTP Server with PHP (supports PHP 5.6, 7, and 8)

This is the primary web hosting component.  Most sites use it.  Users have access to a www root and public-facing docroot where they may deploy any files they wish, including local Apache configuration directives via .htaccess.  This allows them to, for example, enable CGI scripts to run server-side applications.  The web servers have full access to O2's parallel filesystems (/n/groups, /n/data1, etc) as well as slurm and the HPC cluster-- although sites may not submit jobs unless their site's role user has been granted access.

O2 Web Users do not have direct access to the web servers.

#### Apache Tomcat (Java) application servers

Several sites run [Apache Tomcat](https://tomcat.apache.org/), a java-based web application server.  Tomcat seems to have largely fallen out of favor with developers who use O2 Web Hosting, but several legacy Tomcat applications remain.  The most notable sites using Tomcat are www.immgen.org and www.flyrnai.org-- both actively used and maintained research sites.  There are some questionable legacy tomcat sites as well, such as mhl.countway.harvard.edu.  The Tomcat component is a support liabilty DevOps as it relies on very old automation and versions of Java and tomcat.

Tomcat users have shell access to the application servers, where they may start and stop their own applications.

#### Gunicorn (Python) application servers

Python-based web applications using frameworks like Flask and Django became increasingly popular during the 2010s.  Gunicorn is a production-quality server for Python web applications.  Setup and configuration of this component typically requires some coordination between the user and DevOps.  Developers install their code (and Gunicorn itself) into a Python Virtualenv and the O2 Web Gunicorn Framework serves the application to the world.

Gunicorn users are given shell access to their application servers, where they may start and stop their own applications.

#### Generic application servers

This is a generalized variant of the Gunicorn component that allows users run nearly any type of web service.  This component has been used to run Ruby on Rails and Node.JS, as well as the CryoSparc servers (which really qualifies as its on sub-component from a service standpoint).  The CBDM Lab's Rosetta tool will likely use this component.

#### CryoSPARC application server

DevOps provides CryoSPARC instances to several different labs.  CryoSPARC is a scientific web application that submits batch jobs to run Cryo-EM analysis on GPUs.

#### EVCouplings

The Marks Lab EVCouplings service is a complex web application with multiple components.  There are two actively supported versions.  Both have a javascript frontend served by nginx, a python-based API backend and a message queue with worker nodes that submit HPC jobs to the Slurm cluster.  The message queue is implemented using MongoDB in v1, and Redis in v2.  The lab worked closely with Research Computing over several years supporting development of these applications (as well as its predecessor, called EVFold).

