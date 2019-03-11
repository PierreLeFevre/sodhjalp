from flask import (
    Flask, g, redirect, url_for, flash
)

class API:

    def __init__(self):
        pass

    @staticmethod
    def verifyFormLogin( 
            username   =None,
            password   =None,
            email      =None):

        if username is None:
            return 'Username is required'
        elif password is None:
            return 'Password is required'
        elif email is None:
            return 'Email is required'
        
        return None

    @staticmethod
    def verifyFormPost(
            title = None,
            body  = None):

        if title is None:
            return 'Title is required'
        elif body is None:
            return 'Body is required'

        return None

    @staticmethod
    def verifyEmail(email):

        verifyDot = [
            '.com',
            '.se'
        ]

        if list(email).count("@") > 1:
            return "You can only have one '@'"
    
            


            
        
        











