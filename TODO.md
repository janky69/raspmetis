The raspberrypi should produce the equivalent of the following c structure:

```
struct Mvup_t
{
	long lat, lon;
	unsigned long gradi, date, times;
	float vel, attitude[3], tempDS, left, right;
	byte Wspeed, vale_1, vale_2;
};
```

