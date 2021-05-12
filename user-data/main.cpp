#include "users.h"

int main(){
    std::unique_ptr<users::users> newUsers(new users::users(0,"test1"));
    newUsers->addNewUser("berk", 50, true);
    newUsers->checkUser(newUsers->getPublicUserID(i));

}
