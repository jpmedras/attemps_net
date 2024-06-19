# assignment_net
A proposal based on data mining and social networks for visualizing students assignments.

```
python3 src/trivial.py
for y in 2018 2019 2021 2022 2023; do ./assets/png.sh trivial/$y.dot trivial/$y.png; done
```

```
python3 src/students.py
for y in 2018 2019 2021 2022 2023; do ./assets/png.sh students/$y.dot students/$y.png; done
```

```
python3 src/questions.py
for y in 2018 2019 2021 2022 2023; do ./assets/png.sh questions/$y.dot questions/$y.png; done
```