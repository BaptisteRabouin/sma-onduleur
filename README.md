# sma-onduleur
A project I carried out in response to a specific need in my home to automate the sending of an email following an inverter error.

## The problem
On a SMA brand photovoltaic inverter, when the inverter was in error, particularly due to an overvoltage or undervoltage of the electrical network, it would cut itself off without informing me. It was not equipped with the functionality allowing it to automatically reconnect if necessary.

## Solution
I developed a Python script that retrieves information that is only present when the inverter is in error. If this information is present on the inverter's web page, it indicates the inverter is in error. At that moment, the script triggers an email notification to inform me, so I can manually reconnect the inverter.
