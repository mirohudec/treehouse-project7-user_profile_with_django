# User Profile with Django

## Treehouse project 7

For this project, you’ll build a form that takes in details about a registered user and displays those details on a profile page. The profile page should only be visible once the user has logged in.The profile page should include first name, last name, email, date of birth, confirm email, short bio and the option to upload an avatar.

You’ll also set up validation for email, date of birth and the biography. The Date of Birth validation should accept three date formats: YYYY-MM-DD, MM/DD/YYYY, or MM/DD/YY. The Email validation should check if the email addresses match and are in a valid format. The bio validation should check that the bio is 10 characters or longer and properly escapes HTML formatting.

You’ll also create a "change password page" that updates the user’s password. This page will ask for current password, new password and confirm password. Set up validation which checks that the current password is valid, that the new password and confirm password fields match, and that the new password follows the following policy:

must not be the same as the current password
minimum password length of 14 characters.
must use of both uppercase and lowercase letters
must include of one or more numerical digits
must include of special characters, such as @, #, \$
cannot contain the username or parts of the user’s full name, such as his first name

## Comments

### Image Editor

#### From Extra Credit:

##### Image Editor Doesn't work in Firefox

Add an online image editor to the avatar. Include the basic functionality: rotate, crop and flip. PNG mockup supplied.

Don't know if you need to create your own simple editor or get a javascript library or a python django one and implement it.

Decided to create realy simple one myself. I am using Drag and drop API from broswer for the crop functionality. it works in Windows 10 in Chrome, Edge and Opera. Firefox doesn't work because they return different offset in drag event and i dont want to rewrite the whole drag system to mouse movement (It already took at least 2 days for me to implenet this basic editor)
