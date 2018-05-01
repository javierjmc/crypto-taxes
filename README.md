THE SAMPLE CODE ON IN THIS REPOSITORY COM IS PROVIDED “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL UKARLSSON OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION; OR INCORRECTLY GENERATED TAX STATEMENTS) SUSTAINED BY YOU OR A THIRD PARTY, HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT ARISING IN ANY WAY OUT OF THE USE OF THIS SAMPLE CODE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# crypto-taxes

Generate trades info per currency:

```
mkdir -p data/trades && ./kraken_trades.py
```

Check trades
```
jq . < data/trades/LTC.json
```

Use API to annotate trades with value

```
./trades_value.py LTC
```

Check result
```
jq . < data/trades-value/LTC.json
```

Perform tax calculations
```
./trades_calculation.py LTC
```

Check calculations
```
jq . < data/trades-calculations/LTC.json
```

Check summary (this is what needs to go into the K4 form at Skatteverket) as follows:

* expense - omkostnadsbelopp
* value - försäljningsvärde
* amount - antal coins

```
jq . < data/trades-summary/LTC.json
```
