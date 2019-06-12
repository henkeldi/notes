
# Flutter

## Dart

Hello World:

```dart
main() {
  var words = ['Hello', 'world];
  print('${words.join(", ")}!');
}
```

It's object oriented:

```dart
class Griffin extends Lion with Eagle {
  var name;
  Griffin(this.name);
  
  rideTo(dest) {
    print('Riding $name to $dest!');
  }
}

Griffin('Jo').rideTo('Google IO');
```

