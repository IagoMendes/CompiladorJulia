local i::Int
local n::Int
local f::Int

i = 2
n = 5
f = 1

while (i < n + 1)
    f = f * i
    i = i + 1
end

println(f)

if (f > 120)
    println(f)
elseif (f == 120)
    println(f+2)
else
    println(f +1)
end
