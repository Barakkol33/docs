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

### Code Example

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
```

---

# C++

## Basics

C++ is a compiled language that combines low-level memory control with high-level abstractions.

### Example

```cpp
#include <iostream>
#include <string>
#include <cstdint>
#include <algorithm>

int main() {
    uint8_t age = 25;
    uint32_t salary = 100000;
    std::cout << "Age: " << static_cast<int>(age) << std::endl;
    std::cout << "Salary: " << salary << std::endl;

    std::string name;
    std::cout << "Enter your name: ";
    std::getline(std::cin, name);
    std::cout << "Hello, " << name << "!" << std::endl;
}
```

---

## foreach Example

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> nums = {1, 2, 3, 4, 5};

    for (int value : nums)
        std::cout << value << " ";

    std::cout << std::endl;
}
```

---

## References, Move, and Smart Pointers

### std::move Example

```cpp
#include <iostream>
#include <utility>
#include <string>

int main() {
    std::string src = "Hello";
    std::string dest = std::move(src);
    std::cout << dest << std::endl; // "Hello"
}
```

### std::unique_ptr Example

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
}
```

### std::shared_ptr Example

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

## Classes — Rule of 5 Example

```cpp
#include <iostream>
#include <cstring>

class Buffer {
private:
    char* data;
    size_t size;

public:
    Buffer(const char* str) {
        size = std::strlen(str);
        data = new char[size + 1];
        std::strcpy(data, str);
    }

    // Copy constructor
    Buffer(const Buffer& other) {
        size = other.size;
        data = new char[size + 1];
        std::strcpy(data, other.data);
    }

    // Copy assignment
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            delete[] data;
            size = other.size;
            data = new char[size + 1];
            std::strcpy(data, other.data);
        }
        return *this;
    }

    // Move constructor
    Buffer(Buffer&& other) noexcept : data(other.data), size(other.size) {
        other.data = nullptr;
        other.size = 0;
    }

    // Move assignment
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

    ~Buffer() { delete[] data; }

    void print() const { std::cout << data << std::endl; }
};
```

---

## Files — Read and Write

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

---

## Networking — Boost.Asio TCP Example

```cpp
#include <boost/asio.hpp>
#include <iostream>

using boost::asio::ip::tcp;

int main() {
    boost::asio::io_context io;
    tcp::acceptor acceptor(io, tcp::endpoint(tcp::v4(), 12345));

    std::cout << "Server listening..." << std::endl;

    for (;;) {
        tcp::socket socket(io);
        acceptor.accept(socket);
        std::string msg = "Hello from server!\n";
        boost::asio::write(socket, boost::asio::buffer(msg));
    }
}
```

---

# Python

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
packed = struct.pack('<I', 123456)
print(packed)

value, = struct.unpack('<I', packed)
print(value)
```

---

# Security

## Buffer Overflow

**Cause:** Writing past array bounds.
**Prevention:**

* Use `strncpy`, `memcpy_s` in C/C++.
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