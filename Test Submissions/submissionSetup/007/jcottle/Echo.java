import java.util.Scanner;
public class Echo{
    public static void main(String[] args) {
        System.out.println("Hello World");
        Scanner in = new Scanner(System.in);

        while (in.hasNext()){
            System.out.println(in.nextLine());
        }
        
        in.close();
    }
}