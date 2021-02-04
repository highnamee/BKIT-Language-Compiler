.source MCClass.java
.class public MCClass
.super java.lang.Object

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
.var 1 is i I from Label0 to Label1
	iconst_0
	istore_1
Label0:
Label2:
	iload_1
	iconst_4
	if_icmpge Label4
	iconst_1
	goto Label5
Label4:
	iconst_0
Label5:
	ifle Label3
.var 2 is value I from Label0 to Label1
	iconst_2
	istore_2
	iload_1
	iconst_1
	iadd
	istore_1
	iload_1
	iconst_2
	if_icmpne Label8
	iconst_1
	goto Label9
Label8:
	iconst_0
Label9:
	ifle Label6
	goto Label2
	goto Label7
Label6:
Label7:
	iload_2
	invokestatic io/string_of_int(I)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
	goto Label2
Label3:
Label1:
	return
.limit stack 5
.limit locals 3
.end method

.method public <clinit>()V
	return
.limit stack 0
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
