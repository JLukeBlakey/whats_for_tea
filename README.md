# What's for tea?
Based on inputs provided in `recipes.yaml`, creates a schedule of 5 random meals with a shopping list. 'regulars' are added to the list. 

## Setup
Files required:
- `recipes.yaml` contains meals and key-value pairs of ingredients-quantity. 
- `regulars.txt` text items to be added to the shopping list.
-  `.env.emails` to contain key-value pairs, where the values are email addresses the list will be sent to. The key does not matter functionality-wise. See `.env.emails.sample` for an example.
- `.env`  with `smtp_ip` defined, which should be the hostname or IP of the mail server to be used as a relay for sending out mail.

If you do not have a mail server available, please message me with your hostname or IP (must be static) and I can add an allow rule for my mail server to be used.
