from jpype import startJVM, getDefaultJVMPath, JPackage, addClassPath

startJVM(getDefaultJVMPath(), "-ea")
addClassPath("morphy/padeg.jar")
Padeg = JPackage('padeg.lib').Padeg

p = Padeg()
print(p.getOfficePadeg("Менеджеры", 2))