# Odoo-based Drip Marketing Tool

## 1. Introduction

### 1.1 Purpose

The purpose of this document is to outline the software requirements for an Odoo-based Drip Marketing Tool. 
This tool will be built on the existing email marketing module provided by Odoo, leveraging automated and/or scheduled actions to enable a seamless drip marketing experience.

### 1.2 Scope

This document describes the functional and non-functional requirements for the drip marketing module, 
including the creation and management of email "Chains", "Gaps", and Mailing List (ML, or just List) associations.

## 2. System Overview

- The Odoo-based Drip Marketing Tool will allow marketers to create a series of emails called a "Chain." 
- When a user joins a mailing list associated with a Chain, they will receive the emails in the Chain sequentially, with a specified "Gap" between each email. 
- The Gap can vary between subsequent emails in the Chain.

## 3. Functional Requirements

### 3.1 Chain Creation and Management

#### 3.1.1 Create Chain

The system shall allow marketers to create a new Chain by providing the following information:

- Chain name
- Chain description (optional)
- Associated mailing list

#### 3.1.2 Add Email to Chain

The system shall allow marketers to add emails to a Chain. Each email shall have the following attributes:

- Email subject
- Email content (HTML or plain text)
- Preview (same as preview of Settings > Technical > Email-Templates)
- Gap duration (time between this email and the previous email in the chain)

#### 3.1.3 Edit Chain

The system shall allow marketers to edit an existing Chain, including modifying the Chain name, description, content and associated mailing list.

#### 3.1.4 Edit Email in Chain

The system shall allow marketers to edit the attributes of an email in a Chain, including subject, content, and gap duration.

#### 3.1.5 Deactivate Chain

- If there are related Lists or Mails, marketer can only deactivate a Chain.
- Else the Chain can be deleted.

#### 3.1.6 Delete Email from Chain

- The system shall allow marketers to remove an email from a Chain.
- If there are no dependencies, Mail can be deleted.

### 3.2 Mailing List Association

#### 3.2.1 Associate Mailing List with Chain

The tool shall allow marketers to associate a mailing list (List) with a Chain.
Odoo provides comprehensive List management.
Consider related modules [like Contact2MailingList](https://github.com/euroblaze/Contact2MailingList), which adds Odoo Contacts automatically to Lists.
When a user joins the List, they will automatically begin receiving emails from the associated Chain.

#### 3.2.2 Disassociate Mailing List from Chain

Allow marketers to disassociate a mailing list from a Chain.

### 3.3 Email Delivery

#### 3.3.1 First Email

- Marketer can set the Gap (Gap0) before the first Mail in the Chain is sent.
- If Gap0 is not set, the first email in a Chain to a user is sent when they join the associated mailing list.

#### 3.3.2 Scheduled Email Delivery

- The system shall send subsequent emails in a Chain to a user according to the specified Gap durations between emails.
- Scheduler checks if mails have be sent every 400 seconds.

## 4. Non-Functional Requirements

### 4.1 Performance, Security, Scalability, Integration

- The system shall be able to handle at least 10,000 active mailing list subscribers and send emails to all subscribers within 24 hours.
- The system shall adhere to Odoo's existing security protocols and data protection measures.
- The system shall be scalable to accommodate future growth in the number of mailing lists, Chains, and subscribers.
- The system shall integrate seamlessly with Odoo's existing email marketing module.

## Acceptance Criteria

- It should be possible to subscribe to Lists by submitting webform and unsubscribe from Lists by clicking on link in Mails.

## 5. Example

Marketer creates a Chain called "Product Onboarding" with the following emails:

1. "Welcome to our Product" - Gap: 0 (sent immediately upon joining the mailing list)
2. "Getting Started with Product Features" - Gap: 2 days
3. "Advanced Tips and Tricks" - Gap: 5 days
4. "Customer Success Stories" - Gap: 7 days
5. "Exclusive Offer for New Users" - Gap: 10 days

Marketer associates the "Product Onboarding" Chain with a mailing list called "New Subscribers."

When a user joins the "New Subscribers" mailing list, they receive the "Welcome to our Product" email immediately. 
After 2 days, they receive the "Getting Started with Product Features" email. 
Subsequent emails are sent according to the specified Gaps, with the user receiving all emails in the Chain over a span of 24 days.

