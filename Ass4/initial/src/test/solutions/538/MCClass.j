.source MCClass.java
.class public MCClass
.super java.lang.Object
.field static x I

.method public static foo()Z
Label0:
	bipush 110
	putstatic MCClass/x I
	iconst_1
	ireturn
Label1:
.limit stack 2
.limit locals 0
.end method

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label0:
	iconst_1
	ifgt Label5
	invokestatic MCClass/foo()Z
	ifgt Label5
	iconst_0
	goto Label4
Label5:
	iconst_1
Label4:
	ifle Label2
	goto Label3
Label2:
Label3:
	getstatic MCClass/x I
	invokestatic io/string_of_int(I)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
Label1:
	return
.limit stack 5
.limit locals 1
.end method

.method public <clinit>()V
	bipush 120
	putstatic MCClass/x I
	return
.limit stack 1
.limit locals 0
.end method

.method public <init>()V
.var 0 is this LMCClass; from Label0 to Label1
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
Label1:
	return
.limit stack 1
.limit locals 1
.end method
