class Dog
def initialize(name:"5 + 4 * i - (3 + i)", hp:, sleep_level:5 + 4 - (3), pee_level:)
@name = name
@hp = hp
@sleep_level = sleep_level
@pee_level = pee_level
end
def walk(min_hp:, a_reason:)
bark(something_to_say: @name)
@hp -= 1
puts "i walk because #{a_reason}"
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
while (@hp > 1)
@hp -= 2.0
end
puts "guau, guau"
@hp += 10.0
end
end

myDog = Dog.new(hp: 2, pee_level: 100)
myDog.takeashit()
