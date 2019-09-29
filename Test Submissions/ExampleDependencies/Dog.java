public class Dog{
    private String name;
    public Dog(String name){
        this.name = name;
    }

    public void speak(){
        System.out.printf("%s: Bark!\n", name);
    }

    public String toString(){
        return String.format("%s is a dog!", name);
    }
}