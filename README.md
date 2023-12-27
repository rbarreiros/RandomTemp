
Rui Barreiros - rbarreiros <at> gmail <dot> com

## Ultimaker Cura post processing plugin to randomize temperature each layer

```
  Minimum temperature    - minimum allowed temperature for the randomizer

  Maximum temperature    - maximum allower temperature for the randomizer

  Temperature steps**    - temperature interval between maximum and minimum temperature. 
                         the bigger the number, less possible values between min/max
                         temperature, for example, min temp is 200 and max temp is 210
                         if steps are 5, it'll change between 200/205/210, if steps are
                         2, it'll change between 200/202/204/206/208/210

  Layer Start offset     - Layer at which the random temperature start being calculated
                         initial layer (0) + offset, a value of 5 will start the random
                         temperature at layer 5

  Layer End offset       - Layer at which the random temperature stops being calculated
                         last layer - offset, for example, if last layer is 100, and 
                         offset 5, it'll stop at layer 95
```

**_Script not thoroughly tested yet, alpha version, proceed with caution, I'm not responsible
if anything breaks._**
