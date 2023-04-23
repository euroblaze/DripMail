# Drip Marketing Tool for Odoo

An Odoo module that allows marketers to create and manage email chains for drip marketing campaigns, building on top of the Odoo Email Marketing module.

## Overview

The Drip Marketing Tool module is built on top of Odoo's existing email marketing module. It enables marketers to create a series of emails called a "Chain." When a user joins a mailing list associated with a Chain, they will receive the emails in the Chain sequentially, with a specified "Gap" between each email. The Gap can vary between subsequent emails in the Chain.

## Features

- Create and manage email Chains
- Associate mailing lists with Chains
- Automatically send emails in the Chain based on specified Gap intervals
- Integrates seamlessly with Odoo's existing email marketing module

## Installation

1. Download or clone the `drip_marketing_tool` module to the `addons` folder of your Odoo instance.
2. Restart your Odoo server.
3. Go to the "Apps" menu in your Odoo instance, search for "Drip Marketing Tool," and install the module.

## Usage

After installing the module, you can start creating and managing email Chains by navigating to the "Drip Marketing Tool" menu item in the "Marketing" app.

### Creating a Chain

1. Go to the "Drip Marketing Tool" menu.
2. Click on "Create" to create a new Chain.
3. Fill in the Chain name, description (optional), and associated mailing list.
4. Save the Chain.

### Adding Emails to a Chain

1. Go to the "Drip Marketing Tool" menu.
2. Open the Chain you want to add emails to.
3. Click on the "Add Email" button.
4. Fill in the email subject, content, and gap duration (time between this email and the previous email in the chain).
5. Save the email.

### Editing Chains and Emails

1. Go to the "Drip Marketing Tool" menu.
2. Open the Chain or Email you want to edit.
3. Modify the necessary fields and save your changes.

### Deleting Chains and Emails

1. Go to the "Drip Marketing Tool" menu.
2. Select the Chain or Email you want to delete.
3. Click on the "Action" button and choose "Delete."

## Support

For any issues, questions, or suggestions, please open an issue on the GitHub repository or contact the module author.
