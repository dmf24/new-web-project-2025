## O2 Web and App Hosting

## The Service

O2 Web Hosting is a platform enabling the HMS community to create custom PHP and CGI-based applications hosted with Apache HTTP Server or Java Tomcat (via mod_jk), as well as arbitrary applications with http APIs.

The service aims to provide highly available, public-facing HTTP/S endpoints with SSL termination, loadbalancing and redundant backend servers.

## Request/Intake

The O2 Web service entered a "limbo" state some years ago from which it hasn't yet emerge.  There is no standard method to request an O2 Web Service.  Users either submit a general request via STAT, which is routed to DevOps (sometimes via referral from Research Computing); or a need is identified and tasked as part of a project.

Demand history since 2021: 13 new sites per year, 22 sites removed per year


## User Experience

User Experience for O2 Web is, essentially, bundled with O2.  Site owners have an O2 account.  They authenticate and connect to the O2 Login servers to access their docroot or application files, which are secured with O2 posix permissions.  Users generally have extensive ability to develop their own applications, although their access to configure the web services specifically is more limited.  Users with applications have access to restart them.  Apache/PHP users do not.

## Administrative Experience

Configuration is coordinated and automated.  Configuration changes are made through a github repository.

## Dependencies

## Infrastructure

