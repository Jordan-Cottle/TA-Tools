public class DependencyTest{
    public static void main(String[] args) {
        // Requires a Dog file in same directory to function
        Dog dog = new Dog("Toby");

        dog.speak();
        dog.speak();

        System.out.println(dog);
    }
}