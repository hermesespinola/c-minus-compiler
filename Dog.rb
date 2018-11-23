class Person
    def initialize(name:"firulais")
        @name = name
    end
    
    def eat(food:)
        puts "i'm going to eat"
        puts food
    end
    
    def work(energy:)
        if energy < 50
            puts "i can't work"
        end
        if energy > 49
            energy = energy - 10
        end
        return energy
    end
    
    def sleep()
        puts "i am going to sleep"
    end
    
    def want()
        puts "to want is human"
    end
end
    class Dog
    def initialize(name:"firulais", hp:, sleep_level:5 + 4 - (3 + 2), pee_level:)
    @name = name
    @hp = hp
    @sleep_level = sleep_level
    @pee_level = pee_level
    end
    def walk(min_hp:, a_reason:)
    bark(something_to_say: @name)
    if @hp < 100
    return 5 + bark(something_to_say: "heey") - 1 * (4 + 2)
    end
    @hp -= 1
    puts "i walk because"
    return a_reason
    end
    def bark(something_to_say:)
    puts something_to_say
    puts "i mean, bark!"
    end
    def pee()
    @pee_level -= 10.0
    end
    def sleep()
    @sleep_level += 21.0
    end
    def takeashit()
    amount = "way too much"
    walk(min_hp: 11.0, a_reason: "i need to take a shit")
    while @hp > 1
    @hp -= 2.0
    end
    puts "guau, guau"
    @hp += 10.0
    end
    end

hermes = Person.new(name: "Hermes")
puts hermes.work(energy: 49)