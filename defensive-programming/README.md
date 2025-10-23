# Defensive Programming

## Introduction

Defensive programming is a methodology aimed at building resilient and predictable code.

In distributed systems and client-server architectures, errors can occur due to latency, partial failures, and unexpected data — defensive techniques ensure that the system remains correct and recoverable.

---

# Programming Concepts

* **Correctness:** Code should meet its specifications under all valid inputs.
* **Complexity:** Keep algorithms efficient and the codebase simple.
* **Flexibility:** Write modular, reusable components that can evolve.
* **Use Cases:** Define concrete user stories to clarify expected behavior.

---

# Object-Oriented Programming (OOP)

### Core Concepts

* **Class:** Blueprint for objects.
* **Object:** Instance of a class.
* **Encapsulation:** Hide internal state behind public methods.
* **Inheritance:** Reuse and extend base functionality.
* **Polymorphism:** Common interface, different implementations.

### UML

Used to visualize class structure and relationships.

### Data Flow Diagram

Visual representation of how data moves through a system.
It shows where data comes from, where it goes, and how it’s transformed.

```
[User] --> (Login Process) --> [Database]
```

### Code Example

* Abstract base class `Shape`.
* Derived `Circle` overriding `area()`.
* Use of virtual destructor.
* Polymorphism through base pointer.

```cpp
class Shape {
public:
    virtual double area() const = 0; // abstract
    virtual ~Shape() = default;
};

class Circle : public Shape {
private:
    double radius;
public:
    explicit Circle(double r): radius(r) {}
    double area() const override { return 3.1415 * radius * radius; }
};

int main() {
    Shape* shape = new Circle(5.0);   // dynamic polymorphism
    std::cout << "Circle area: " << shape->area() << std::endl;
    delete shape;                     // clean up
    return 0;
}
```

---

# C++ (aka Cpp)

## Basics

Cpp is a compiled language that combines low-level memory control with high-level abstractions.

Imporant note: It has no garbage collector, so it is up to the user to plan objects destruction and memory cleanup.

```cpp
#include <iostream>
#include <string>
#include <cstdint>
#include <algorithm>

int main() {
    // Well-defined number types. 
    uint8_t age = 25;
    uint32_t salary = 100000;
    uint32_t max = std::max(1,3);
    uint32_t min = std::min(1,3);

    // I/O
    std::cout << "Age: " << age << std::endl;
    std::cout << "Salary: " << salary << std::endl;

    std::string name;
    std::cout << "Enter your name: ";
    std::cin >> name;
    // Also valid: std::getline(std::cin, name);
    std::cout << "Hello, " << name << "!" << std::endl;

    // foreach 
    std::vector<int> nums = {1, 2, 3, 4, 5};
    for (int value : nums) { 
        std::cout << value << " ";
    }
    std::cout << std::endl;

    // strings
    std::string text = "hello world";
    // length()
    std::cout << "Length: " << text.length() << std::endl;
    // substr()
    std::string sub = text.substr(0, 5); // "hello"
    // find()
    size_t pos = text.find("world");
    if (pos != std::string::npos) {
        std::cout << "'world' found at position " << pos << std::endl;
    }

    // numbers <--> strings
    int num = 42;
    std::string str = std::to_string(num);

    std::string text = "123";
    int n = std::stoi(text);
    double d = std::stod("3.14");
}
```

--- 

## Cpp Runtime Memory Layout — Stack, Heap, Code, and Growth Direction

When a Cpp program runs, memory is divided into regions:

| Region                      | Purpose                                                         | Example                                         |
| --------------------------- | --------------------------------------------------------------- | ----------------------------------------------- |
| **Code / Text Segment**     | Stores compiled instructions (functions).                       | `main()` machine code lives here.               |
| **Static / Global Segment** | Stores global and static variables.                             | `static int counter = 0;`                       |
| **Heap**                    | Dynamically allocated memory (`new`, `malloc`, smart pointers). | `int* p = new int(10);`                         |
| **Stack**                   | Function calls, local variables, return addresses.              | Inside `main()`, local `int x = 5;` lives here. |

### Growth Direction

* **Stack** grows **downward** (toward lower memory addresses).
* **Heap** grows **upward** (toward higher addresses).
  They expand toward each other — a full memory collision = stack/heap overflow.

```
| high addresses |
+----------------+
|   Stack (↓)    |
|----------------|
|      ...       |
|----------------|
|   Heap (↑)     |
+----------------+
| low addresses  |
```

---

## Endianness: Little Endian Explained

**Little Endian** means the **least significant byte (LSB)** is stored first (at the lowest address).

Example:

```cpp
int x = 0x12345678;
```

Memory layout (addresses increasing →):

```
78 56 34 12
```

**Big Endian** would store:

```
12 34 56 78
```

Most modern PCs (x86, ARM) are **Little Endian**.

---

## Manual Memory Management - `new` / `delete`

```cpp
#include <iostream>

int main() {
    int* num = new int(42); // allocate memory
    std::cout << "Value: " << *num << std::endl;

    *num = 100;             // modify value
    std::cout << "New Value: " << *num << std::endl;

    delete num;             // free memory
    num = nullptr;          // avoid dangling pointer

    Dog* d = new Dog(); // create object on heap
    d->bark();
    delete d;           // must delete manually

    return 0;
}
```

---

## References, Move, and Smart Pointers

| Term                                 | Definition                                                                                          | Example                              |
| ------------------------------------ | --------------------------------------------------------------------------------------------------- | ------------------------------------ |
| **lvalue reference (`T&`)**          | Refers to an existing object (has address).                                                         | `int x = 5; int& r = x;`             |
| **rvalue reference (`T&&`)**         | Refers to a temporary or movable value. Used for move semantics.                                    | `int&& temp = 10;`                   |
| **`std::move`**                      | Casts an lvalue to an rvalue reference, allowing resources to be moved.                             | `vec2 = std::move(vec1);`            |
| **Smart pointer vs Regular pointer** | Smart pointers manage memory automatically; raw pointers require manual `delete` - Shouldn't be used together to avoid bugs.                   | `new/delete` vs `std::unique_ptr`    |
| **`std::unique_ptr`**                | Smart pointer that owns an object exclusively (no copies). Automatically deletes when out of scope. | `auto p = std::make_unique<int>(5);` |
| **`std::shared_ptr`**                | Smart pointer that uses reference counting; multiple owners.                                        | `auto p = std::make_shared<int>(5);` |

### `std::unique_ptr` Example

```cpp
#include <memory>
#include <iostream>

struct Node {
    int value;
    explicit Node(int v): value(v) {}
};

int main() {
    std::unique_ptr<Node> ptr = std::make_unique<Node>(42);
    std::cout << ptr->value << std::endl;
    // In order to pass value - pointer must be moved.
    // From now on ptr can't be used - points to nothing.
    std::unique_ptr<Node> ptr2 = std::move(ptr);
    std::cout << ptr2->value << std::endl;

    // Can also be given a "raw" pointer.
    std::unique_ptr<Node> ptr2(new Node(43));
}
```

### `std::shared_ptr` Example

```cpp
#include <memory>
#include <iostream>

struct Resource {
    ~Resource() { std::cout << "Freed\n"; }
};

int main() {
    std::shared_ptr<Resource> r1 = std::make_shared<Resource>();
    std::shared_ptr<Resource> r2 = r1;
    std::cout << "Use count: " << r1.use_count() << std::endl;
}
```

---

## Classes 
- `const` function - means that object properties cannot be changed.
  `const` reference to object - only `const` functions can be used.

```cpp
#include <iostream>
#include <cstring>
#include <string>

// ---------------- Base Abstract Class ----------------
class Printable {
public:
    // Abstract (pure virtual)
    virtual void print() const = 0;
    virtual ~Printable() = default;
};

// ---------------- Buffer Class ----------------
class Buffer : public Printable {
private:
    char* data;
    size_t size;

    // Private functions
    void _allocate(const char* str) {
        size = std::strlen(str);
        data = new char[size + 1];
        std::strcpy(data, str);
    }

public:
    // Constructors - Rule of 5
    // Regular (not counted)
    Buffer(const char* str) { _allocate(str); }
    // Copy
    Buffer(const Buffer& other) { _allocate(other.data); }
    // Operator=
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            delete[] data;
            _allocate(other.data);
        }
        return *this;
    }
    // Move
    Buffer(Buffer&& other) noexcept : data(other.data), size(other.size) {
        other.data = nullptr;
        other.size = 0;
    }
    // Move operator=
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data;
            data = other.data;
            size = other.size;
            other.data = nullptr;
            other.size = 0;
        }
        return *this;
    }
    // Virtual destructor
    ~Buffer() override { delete[] data; }

    // Overloaded method: one prints, one with prefix
    void print() const override { std::cout << data << std::endl; }
    void print(const std::string& prefix) const { std::cout << prefix << data << std::endl; }

    // Public functions
    const char* c_str() const { return data; }
    size_t length() const { return size; }

    // Friend operators
    friend std::ostream& operator<<(std::ostream& stream, const Buffer& buf) {
        return stream << buf.data;
    }

    friend Buffer operator*(int times, const Buffer& buf) {
        std::string s;
        for (int i = 0; i < times; ++i)
            s += buf.data;
        return Buffer(s.c_str());
    }
};

// ---------------- Derived Class ----------------
class UpperBuffer : public Buffer {
public:
    // Constructors...
    UpperBuffer(const char* str) : Buffer(str) {}    

    void print() const override {
        std::string temp = c_str();
        for (char& c : temp)
            c = std::toupper(c);
        std::cout << temp << std::endl;
    }
};

// ---------------- Usage ----------------
int main() {
    std::cout << "=== Base buffer ===\n";
    Buffer b1("Hello");
    b1.print();

    std::cout << "\n=== Prefix print ===\n";
    b1.print("Prefix: ");

    std::cout << "\n=== Operator * ===\n";
    Buffer b2 = 3 * b1;
    std::cout << b2 << std::endl;

    std::cout << "\n=== Derived class ===\n";
    UpperBuffer ub("hello world");
    ub.print();  // prints uppercase

    return 0;
}
```

## VTABLE — Virtual Function Table

### 🔹 What it is

A **vtable** (virtual table) is a hidden mechanism that Cpp uses to implement **runtime polymorphism** for classes with **virtual functions**.

When a class has at least one `virtual` function:

* The compiler generates a **vtable** — a table of function pointers.
* Each object of that class stores a hidden pointer (`vptr`) to its class’s vtable.
* At runtime, the correct function is called through that table, based on the actual type of the object (not the pointer type).
* The vtable is essentially an array of pointers to functions and is located at offset 0 of the object's memory.

---

### Example

```cpp
#include <iostream>

class Base {
public:
    virtual void speak() const { std::cout << "Base speaks\n"; }
    virtual ~Base() = default;
};

class Derived : public Base {
public:
    void speak() const override { std::cout << "Derived speaks\n"; }
};

int main() {
    Base* obj = new Derived();
    obj->speak(); // dynamically calls Derived::speak via vtable
    delete obj;
}
```

**Output:**

```
Derived speaks
```

If there were no `virtual`, it would instead call `Base::speak()` (static binding).
So the **vtable** enables **dynamic dispatch**.

In memory, the bytes at `*obj` are the pointer to `Derived::speak()`.

If there were more function their pointers would be at *(obj + 4), *(obj + 8), etc (assuming 32 bit architecture).


-- 

## Environment 
Windows: `_dupenv_s(&variable_value, &value_length, "VARIABLE")`

Linux: `char* variable_value = getenv("VARIABLE")`

---

## Files

```cpp
#include <fstream>
#include <iostream>
#include <string>

int main() {
    // Write to file
    std::ofstream out("example.txt");
    out << "Hello, file!" << std::endl;
    out.close();

    // Read from file
    std::ifstream in("example.txt");
    std::string line;
    while (std::getline(in, line))
        std::cout << line << std::endl;
    in.close();
}
```

## **`std::map` — Key–Value Operations**

```cpp
#include <iostream>
#include <map>
#include <string>

int main() {
    // === 1. Constructors ===
    std::map<std::string, int> ages;  // empty map

    // Initializer list constructor
    std::map<std::string, int> scores = {
        {"Alice", 90},
        {"Bob", 85},
        {"Charlie", 95}
    };

    // Copy constructor
    std::map<std::string, int> copyScores(scores);

    // === 2. Insert and Assign ===
    // Cpp17 insert_or_assign - always updates value (even if exists)
    ages.insert_or_assign("Tom", 31);
    ages.insert_or_assign("Spike", 40);

    // === 3. Access ===
    std::cout << "\nAccess by key:" << std::endl;
    // at() throws exception if key not found - better than []
    std::cout << "Tom: " << ages.at("Tom") << std::endl;

    // === 4. Iteration ===
    std::cout << "\nAll entries:" << std::endl;
    for (const auto& items : ages)
        std::cout << items.first << " -> " << items.second << std::endl;

    // === 5. Find and Erase ===
    auto it = ages.find("Spike");
    if (it != ages.end()) {
        std::cout << "\nErasing: " << it->first << std::endl;
        ages.erase(it);
    }

    return 0;
}
```

## `std::vector` — Dynamic Array Operations

```cpp
#include <iostream>
#include <vector>
#include <algorithm> // for std::find

int main() {
    // === 1. Constructors ===
    std::vector<int> v1;                   // empty
    std::vector<int> v2(5, 42);            // {42,42,42,42,42}
    std::vector<int> v3 = { 1, 2, 3, 4, 5 }; // initializer list
    std::vector<int> v4(v3.begin(), v3.end()); // copy from range

    // === 2. push_back / emplace_back ===
    v1.push_back(10);
    v1.push_back(20);
    v1.emplace_back(30);  // constructs in-place

    std::cout << "v1 contents: ";
    for (int x : v1) std::cout << x << " ";
    std::cout << std::endl;

    // === 3. Access ===
    // at() is better than [] - throws std::out_of_range on error
    std::cout << "Second element (at()): " << v3.at(1) << std::endl;

    // === 4. Iteration ===
    std::cout << "v3 elements: ";
    for (auto it = v3.begin(); it != v3.end(); ++it)
        std::cout << *it << " ";
    std::cout << std::endl;

    // === 5. find() ===
    auto it = std::find(v3.begin(), v3.end(), 3);
    if (it != v3.end())
        std::cout << "Found 3 at index " << (it - v3.begin()) << std::endl;

    // === 6. Append another vector ===
    std::vector<int> chunk = { 6, 7, 8 };
    v3.insert(v3.end(), chunk.begin(), chunk.end());
    std::cout << "After append: ";
    for (int x : v3) std::cout << x << " ";
    std::cout << std::endl;

    // === 7. Erase elements ===
    v3.erase(v3.begin(), v3.begin() + 2);  // erase first two
    std::cout << "After erase first 2: ";
    for (int x : v3) std::cout << x << " ";
    std::cout << std::endl;

    // === 8. Other useful methods ===
    std::cout << "Size: " << v3.size() << std::endl;
    std::cout << "Front: " << v3.front() << ", Back: " << v3.back() << std::endl;

    return 0;
}
```

---

## Networking — Boost.Asio Example

### Server

```cpp
#include <boost/asio.hpp>
#include <iostream>
#include <string>

using boost::asio::ip::tcp;

int main() {
    try {
        boost::asio::io_context io;
        tcp::acceptor acceptor(io, tcp::endpoint(tcp::v4(), 12345));

        std::cout << "Server listening on port 12345...\n";

        for (;;) {
            tcp::socket socket(io);
            acceptor.accept(socket);

            std::cout << "Client connected!\n";

            // Read message from client
            boost::asio::streambuf buf;
            boost::asio::read_until(socket, buf, '\n');
            std::string client_msg = boost::asio::buffer_cast<const char*>(buf.data());
            std::cout << "Received from client: " << client_msg;

            // Reply to client
            std::string response = "Server received: " + client_msg;
            boost::asio::write(socket, boost::asio::buffer(response));
        }
    } catch (std::exception& e) {
        std::cerr << "Server error: " << e.what() << std::endl;
    }
}
```

---

### Client

```cpp
#include <boost/asio.hpp>
#include <iostream>
#include <string>

using boost::asio::ip::tcp;

int main() {
    try {
        boost::asio::io_context io;
        tcp::socket socket(io);
        socket.connect(tcp::endpoint(boost::asio::ip::make_address("127.0.0.1"), 12345));

        std::cout << "Connected to server.\n";

        // Send message
        std::string msg = "Hello from client!\n";
        boost::asio::write(socket, boost::asio::buffer(msg));

        // Read response
        boost::asio::streambuf buf;
        boost::asio::read_until(socket, buf, '\n');
        std::string response = boost::asio::buffer_cast<const char*>(buf.data());
        std::cout << "Response from server: " << response << std::endl;

    } catch (std::exception& e) {
        std::cerr << "Client error: " << e.what() << std::endl;
    }
}
```

### cryptopp
Download and extract -https://www.cryptopp.com/ -> Downloads

Build and add lib to link libraries, add directory as include directory.

### boost
Download and extract - https://www.boost.org/releases/latest/

Note: To use `asio` you don't need to build it.

---

# Python

## Docs
https://docs.python.org/3/tutorial

## Networking with select Example

```python
import socket, select

server = socket.socket()
server.bind(('0.0.0.0', 5000))
server.listen()

sockets = [server]
print("Listening...")

while True:
    readable, _, _ = select.select(sockets, [], [])
    for s in readable:
        if s is server:
            conn, addr = s.accept()
            sockets.append(conn)
            print("New connection:", addr)
        else:
            data = s.recv(1024)
            if not data:
                sockets.remove(s)
                s.close()
            else:
                print("Received:", data.decode())
```

---

## Struct — Little Endian Example

```python
import struct

# < means little endian
packed = struct.pack('<L', 123456)
print(packed)

value, = struct.unpack('<L', packed)
print(value)
```

---

# Security

## Buffer Overflow

**Cause:** Writing past array bounds.

**Prevention:**

* Use `strncpy`, `memcpy_s` in C/Cpp.
* Enable **stack canaries** and **ASLR**.
* Use safe containers like `std::string`.

---

## Side-Channel Attacks

**Cause:** Leaking info via timing or power analysis.

**Prevention:**

* Use constant-time cryptographic operations.
* Isolate sensitive code (TPM, hardware modules).

---

## Denial of Service (DoS)

**Cause:** Flooding server with requests.

**Prevention:**

* Rate limiting.
* Timeouts and circuit breakers.
* Use non-blocking I/O (e.g. `select`, reactor pattern).

---

## SQL Injection

**Cause:** Unsanitized user input.

**Prevention:**

* Use parameterized queries (`cursor.execute(query, params)`).
* Validate input types.
* Escape strings safely.

---

## Heap Spraying

**Cause:** Filling heap with attacker-controlled data to predict memory layout.

**Prevention:**

* Enable ASLR and DEP.
* Use safe allocators.
* Randomize heap structures.

---

## Return Oriented Programming (ROP)

**Cause:** Reusing existing code (gadgets) for malicious execution.

**Prevention:**

* Enable ASLR and Control Flow Integrity.
* Use non-executable stack/heap.
* Maintain shadow stack integrity.

---

## Remote Code Execution (RCE)

**Cause:** Unsafely executing user-supplied code.

**Prevention:**

* Never use `eval` or `exec` on untrusted data.
* Disable imports: `exec(code, {'__builtins__': None}, {})`.
* Use sandboxing or virtual machines.

---

## Summary of Protections

| Attack          | Protection                                 |
| --------------- | ------------------------------------------ |
| Buffer Overflow | Stack canary, ASLR, bounds checking        |
| Side Channel    | Constant-time operations, TPM              |
| DoS             | Rate limiting, async I/O                   |
| SQL Injection   | Parameterized queries                      |
| Heap Spraying   | ASLR, DEP                                  |
| ROP             | Non-executable memory, CFI                 |
| RCE             | Sandbox, disable `eval`, restrict builtins |

---

# Encryption

## Symmetric

* Shared key between sender and receiver.
* Algorithms: **AES**, **ChaCha20**
* Exchange key via **Diffie-Hellman**.

## Asymmetric

* **Public key** for encryption, **private key** for decryption.
* Used in **TLS/SSL** for key exchange and identity verification.

---